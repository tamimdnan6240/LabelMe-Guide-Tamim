import os
import json
import glob
from PIL import Image, ImageDraw

# === CONFIG ===
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
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # === CLEAN imagePath ===
        original_path = data.get('imagePath', '')
        image_file_name = os.path.basename(original_path)
        data['imagePath'] = image_file_name

        # Overwrite cleaned JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        cleaned += 1

        # === LOAD IMAGE ===
        image_path = os.path.join(os.path.dirname(json_path), image_file_name)
        if not os.path.exists(image_path):
            print(f"⚠️ Image not found: {image_path}")
            continue

        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        # === GET LABEL (first one only for folder naming) ===
        first_label = data['shapes'][0]['label']
        class_folder = os.path.join(output_root, first_label)
        os.makedirs(class_folder, exist_ok=True)

        # === DRAW ANNOTATIONS ===
        for shape in data['shapes']:
            points = shape['points']
            label = shape['label']
            if len(points) == 2:  # bounding box
                draw.rectangle([tuple(points[0]), tuple(points[1])], outline='red', width=3)
                draw.text(tuple(points[0]), label, fill='red')
            else:  # polygon
                draw.polygon([tuple(p) for p in points], outline='blue')
                draw.text(tuple(points[0]), label, fill='blue')

        # === SAVE TO CLASS FOLDER ===
        save_name = os.path.splitext(image_file_name)[0] + "_annotated.jpg"
        save_path = os.path.join(class_folder, save_name)
        image.save(save_path)
        converted += 1

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

print(f"\n✅ Cleaned 'imagePath' in {cleaned} JSON file(s).")
print(f"✅ Saved {converted} annotated image(s) into label-based folders under: {output_root}")
