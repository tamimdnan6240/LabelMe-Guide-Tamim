import os
import json
import glob
import re
from PIL import Image
from sklearn.model_selection import train_test_split

# === CONFIGURATION ===

# Path to the root folder containing annotated images and JSON label files
input_root = r"C:\Users\tadnan\Downloads\Original-data\Original-data\Inclusion-exclusion-dataset"

# Output folders for YOLOv8-compatible image and label data
output_root = os.path.join(input_root, "YOLOv8-ready")
image_out = os.path.join(output_root, "images")  # Where images will be saved
label_out = os.path.join(output_root, "labels")  # Where YOLO .txt files will be saved

# Create output directories if they don't exist
os.makedirs(image_out, exist_ok=True)
os.makedirs(label_out, exist_ok=True)

# === CLASS MAPPING ===

# Maps each unique class name (e.g., "train", "pedestrian") to a numeric ID
class_map = {}
class_index = 0

# === HELPER FUNCTIONS ===

# Cleans up class labels for safe file naming (removes special characters)
def clean_label(label):
    return re.sub(r'[\\/:*?"<>|]', '_', label.strip())

# Converts a polygon or rectangle into YOLO-style bounding box format:
# (x_center, y_center, width, height) all normalized to [0,1]
def get_yolo_bbox(points, img_w, img_h):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # Normalize coordinates to image size
    x_center = (x_min + x_max) / 2.0 / img_w
    y_center = (y_min + y_max) / 2.0 / img_h
    width = (x_max - x_min) / img_w
    height = (y_max - y_min) / img_h

    return x_center, y_center, width, height

# === MAIN PROCESSING LOOP ===

# Locate all .json annotation files recursively
json_files = glob.glob(os.path.join(input_root, '**', '*.json'), recursive=True)
print(f"🔍 Found {len(json_files)} JSON file(s).")

saved = 0  # Counter for successfully processed files

for json_path in json_files:
    try:
        # === LOAD AND CLEAN JSON ===

        # Read and fix path references in the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            raw = f.read().replace('T:/', '').replace('T:\\', '').replace('V:/', '').replace('V:\\', '')
        data = json.loads(raw)

        shapes = data.get('shapes', [])
        if not shapes:
            continue  # Skip if no annotation shapes present

        original_image_path = data.get('imagePath', '')
        image_file_name = os.path.basename(original_image_path)
        data['imagePath'] = image_file_name  # Use only the image filename

        # Construct the full path to the image file
        image_path = os.path.join(os.path.dirname(json_path), image_file_name)
        if not os.path.exists(image_path):
            continue  # Skip if image is missing

        # === LOAD IMAGE AND SAVE TO OUTPUT ===

        image = Image.open(image_path).convert("RGB")
        img_w, img_h = image.size
        new_img_path = os.path.join(image_out, image_file_name)
        image.save(new_img_path)

        # === CONVERT AND SAVE LABELS ===

        label_txt = os.path.join(label_out, image_file_name.replace(".jpg", ".txt"))
        with open(label_txt, 'w') as out_f:
            for shape in shapes:
                label = shape.get('label', '').strip()
                points = shape.get('points', [])
                if not label or not points:
                    continue

                # Assign unique class ID if it's not already in the map
                label_clean = clean_label(label.lower())
                if label_clean not in class_map:
                    class_map[label_clean] = class_index
                    class_index += 1
                class_id = class_map[label_clean]

                # Convert polygon/rectangle to YOLO bbox format
                x_center, y_center, width, height = get_yolo_bbox(points, img_w, img_h)

                # Save in YOLO format: <class_id> <x_center> <y_center> <width> <height>
                out_f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        saved += 1
        print(f"✅ Saved image + label: {image_file_name}")

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

# === SAVE CLASS INDEX LIST FOR REFERENCE ===

with open(os.path.join(output_root, "classes.txt"), "w") as f:
    for cls, idx in sorted(class_map.items(), key=lambda x: x[1]):
        f.write(f"{idx}: {cls}\n")

# === SUMMARY ===

print(f"\n✅ {saved} images converted to YOLO format.")
print(f"📂 Output saved in: {output_root}")

