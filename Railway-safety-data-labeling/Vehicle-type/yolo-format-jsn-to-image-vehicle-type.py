import os
import json
import glob
import re
from PIL import Image

# === CONFIGURATION ===

input_root = r"C:\Users\tadnan\Downloads\Labeled-data\Vehicle-type-dataset\JSON-Vehicle-type"
output_root = r"C:\Users\tadnan\Downloads\Labeled-data\Vehicle-type-dataset"

# Output folders for YOLOv8-compatible image and label data
output_dir = os.path.join(output_root, "YOLOv8-vehicle-type-labeled-dataset")
image_out = os.path.join(output_dir, "images")
label_out = os.path.join(output_dir, "labels")

# Create output directories if they don't exist
os.makedirs(image_out, exist_ok=True)
os.makedirs(label_out, exist_ok=True)

# === CLASS MAPPING ===
class_map = {}
class_index = 0

# === HELPER FUNCTIONS ===

def clean_label(label):
    return re.sub(r'[\\/:*?"<>|]', '_', label.strip())

def get_yolo_bbox(points, img_w, img_h):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    x_center = (x_min + x_max) / 2.0 / img_w
    y_center = (y_min + y_max) / 2.0 / img_h
    width = (x_max - x_min) / img_w
    height = (y_max - y_min) / img_h

    return x_center, y_center, width, height

# === MAIN PROCESSING LOOP ===

json_files = glob.glob(os.path.join(input_root, '**', '*.json'), recursive=True)
print(f"🔍 Found {len(json_files)} JSON file(s).")

saved = 0

for json_path in json_files:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw = f.read().replace('T:/', '').replace('T:\\', '').replace('V:/', '').replace('V:\\', '')
        data = json.loads(raw)

        shapes = data.get('shapes', [])
        if not shapes:
            continue

        original_image_path = data.get('imagePath', '')
        image_file_name = os.path.basename(original_image_path)
        image_path = os.path.join(os.path.dirname(json_path), image_file_name)
        if not os.path.exists(image_path):
            continue

        # Save the image
        image = Image.open(image_path).convert("RGB")
        img_w, img_h = image.size
        new_img_path = os.path.join(image_out, image_file_name)
        image.save(new_img_path)

        # Get base filename for label file
        base_name = os.path.splitext(image_file_name)[0]
        label_txt = os.path.join(label_out, base_name + ".txt")

        with open(label_txt, 'w') as out_f:
            for shape in shapes:
                label = shape.get('label', '').strip()
                points = shape.get('points', [])
                if not label or not points:
                    continue

                label_cleaned = clean_label(label.lower())
                if label_cleaned not in class_map:
                    class_map[label_cleaned] = class_index
                    class_index += 1
                class_id = class_map[label_cleaned]

                x_center, y_center, width, height = get_yolo_bbox(points, img_w, img_h)
                out_f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        saved += 1
        print(f"✅ Saved image + label: {image_file_name}")

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

# === SAVE CLASS INDEX LIST ===
with open(os.path.join(output_dir, "classes.txt"), "w") as f:
    for cls, idx in sorted(class_map.items(), key=lambda x: x[1]):
        f.write(f"{idx}: {cls}\n")

# === SUMMARY ===
print(f"\n✅ {saved} images converted to YOLO format.")
print(f"📂 Output saved in: {output_dir}")
