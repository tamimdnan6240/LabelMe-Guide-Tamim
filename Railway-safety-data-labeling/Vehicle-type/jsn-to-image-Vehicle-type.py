import os
import json
import glob
import re
from PIL import Image, ImageDraw

# === CONFIG ===
input_root = r"C:\Users\tadnan\Downloads\Labeled-data\Vehicle-type-dataset"
output_root = os.path.join(input_root, "CNN-Vehicle-type-labeled-dataset")
os.makedirs(output_root, exist_ok=True)

# === SANITIZER: make label safe for folder names ===
def clean_label(label):
    return re.sub(r'[\\/:*?"<>|]', '_', label.strip())

# === FIND JSON FILES ===
json_files = glob.glob(os.path.join(input_root, '**', '*.json'), recursive=True)
print(f"🔍 Found {len(json_files)} JSON file(s).")

cleaned = 0
converted = 0

for json_path in json_files:
    try:
        # === FIX RAW JSON STRING BEFORE LOADING ===
        with open(json_path, 'r', encoding='utf-8') as f:
            raw = f.read().replace('T:/', '').replace('T:\\', '').replace('V:/', '').replace('V:\\', '')
        data = json.loads(raw)

        shapes = data.get('shapes', [])
        if not shapes:
            print(f"⚠️ No annotations found in: {json_path}")
            continue

        # === CLEAN IMAGE PATH ===
        original_image_path = data.get('imagePath', '')
        image_file_name = os.path.basename(original_image_path)
        data['imagePath'] = image_file_name

        # Save cleaned JSON back
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        cleaned += 1

        # === LOAD IMAGE ===
        image_path = os.path.join(os.path.dirname(json_path), image_file_name)
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            continue

        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        # === CLEAN FIRST LABEL (for folder name) ===
        first_label_raw = shapes[0].get('label', '')
        first_label = clean_label(first_label_raw)
        if not first_label:
            print(f"⚠️ Skipping {json_path}: label missing or invalid")
            continue

        class_folder = os.path.join(output_root, first_label)
        os.makedirs(class_folder, exist_ok=True)

        # === DRAW SHAPES ===
        for shape in shapes:
            label = shape.get('label', '').strip()
            points = shape.get('points', [])
            if not label or not points:
                continue
            if len(points) == 2:
                draw.rectangle([tuple(points[0]), tuple(points[1])], outline='red', width=3)
                draw.text(tuple(points[0]), label, fill='red')
            else:
                draw.polygon([tuple(p) for p in points], outline='blue')
                draw.text(tuple(points[0]), label, fill='blue')

        # === SAVE ANNOTATED IMAGE ===
        save_name = os.path.splitext(image_file_name)[0] + "_annotated.jpg"
        save_path = os.path.join(class_folder, save_name)
        image.save(save_path)
        converted += 1
        print(f"✅ Saved: {save_path}")

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

print(f"\n✅ Cleaned and fixed {cleaned} JSON file(s).")
print(f"✅ Annotated {converted} image(s) saved in: {output_root}")
