import os
import json
import glob
from PIL import Image, ImageDraw

# === CONFIGURATION ===
input_root = r"C:\Users\tadnan\Downloads\final-dataset"
output_root = os.path.join(input_root, "annotated_images_by_label")
os.makedirs(output_root, exist_ok=True)

# === FIND JSON FILES ===
json_files = glob.glob(os.path.join(input_root, '**', '*.json'), recursive=True)
print(f"🔍 Found {len(json_files)} JSON file(s).")

cleaned = 0
converted = 0

for json_path in json_files:
    try:
        # === LOAD & CLEAN JSON ===
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Skip if no annotations
        shapes = data.get('shapes', [])
        if not shapes:
            print(f"⚠️ No annotations found in: {json_path}")
            continue

        # Clean imagePath (convert to just filename)
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
            print(f"❌ Image not found: {image_path} (referenced in {json_path})")
            continue

        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        # === LABEL FOLDER ===
        first_label = shapes[0].get('label', '').strip()
        if not first_label:
            print(f"⚠️ Missing label in: {json_path}")
            continue

        class_folder = os.path.join(output_root, first_label)
        os.makedirs(class_folder, exist_ok=True)

        # === DRAW ANNOTATIONS ===
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
        print(f"✅ Annotated image saved: {save_path}")

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

print(f"\n✅ Cleaned and verified {cleaned} JSON file(s).")
print(f"✅ Saved {converted} annotated image(s) into: {output_root}")
