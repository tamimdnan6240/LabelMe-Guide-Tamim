import os
import json
import glob
import re
from PIL import Image

# === CONFIGURATION ===
input_root = r"C:\Users\tadnan\Downloads\Labeled-data\Inclusion-exclusion-dataset"

# 🔁 Change this for other binary tasks (e.g., 'Train', 'Pedestrian')
target_class_name = "Vehicle"

# Output root folder with clear name
output_root = os.path.join(input_root, f"YOLOv8-ready-{target_class_name.lower()}-detection")

# Output directories
target_img_dir = os.path.join(output_root, target_class_name, "images")
target_lbl_dir = os.path.join(output_root, target_class_name, "labels")
nontarget_img_dir = os.path.join(output_root, f"No_{target_class_name}", "images")
nontarget_lbl_dir = os.path.join(output_root, f"No_{target_class_name}", "labels")

# Create output directories
os.makedirs(target_img_dir, exist_ok=True)
os.makedirs(target_lbl_dir, exist_ok=True)
os.makedirs(nontarget_img_dir, exist_ok=True)
os.makedirs(nontarget_lbl_dir, exist_ok=True)

def clean_label(label):
    return re.sub(r'[\\/:*?"<>|]', '_', label.strip())

def get_yolo_bbox(points, img_w, img_h):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # Fix invalid bounding boxes
    if x_max < x_min or y_max < y_min:
        x_min, x_max = min(x_min, x_max), max(x_min, x_max)
        y_min, y_max = min(y_min, y_max), max(y_min, y_max)

    x_center = (x_min + x_max) / 2.0 / img_w
    y_center = (y_min + y_max) / 2.0 / img_h
    width = (x_max - x_min) / img_w
    height = (y_max - y_min) / img_h
    return x_center, y_center, width, height

# === MAIN LOOP ===
json_files = glob.glob(os.path.join(input_root, '**', '*.json'), recursive=True)
print(f"🔍 Found {len(json_files)} JSON file(s).")

# 🚗 Set labels related to Vehicle here (update for Train, Pedestrian later)
vehicle_labels = {
    "vehicle", "passenger vehicle", "commercial truck", 
    "bus", "emergency or utility vehicle", "multiclass vehicle"
}

saved = 0

for json_path in json_files:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        shapes = data.get('shapes', [])
        if not shapes:
            continue

        original_image_path = data.get('imagePath', '')
        image_file_name = os.path.basename(original_image_path)
        image_path = os.path.join(os.path.dirname(json_path), image_file_name)
        if not os.path.exists(image_path):
            continue

        # Check if any label is in the vehicle set
        labels_in_image = {clean_label(shape.get("label", "").lower()) for shape in shapes}
        is_target = any(label in vehicle_labels for label in labels_in_image)

        # Decide output path
        img_out = target_img_dir if is_target else nontarget_img_dir
        lbl_out = target_lbl_dir if is_target else nontarget_lbl_dir

        # Save image
        image = Image.open(image_path).convert("RGB")
        img_w, img_h = image.size
        new_img_path = os.path.join(img_out, image_file_name)
        image.save(new_img_path)

        # Save label
        label_txt = os.path.join(lbl_out, image_file_name.replace(".jpg", ".txt").replace(".png", ".txt"))
        with open(label_txt, 'w') as out_f:
            for shape in shapes:
                label = clean_label(shape.get('label', '').lower())
                points = shape.get('points', [])
                if not points:
                    continue
                x_center, y_center, width, height = get_yolo_bbox(points, img_w, img_h)

                class_id = 0 if is_target else 1  # binary: 0 = target, 1 = no target
                out_f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        saved += 1
        print(f"✅ Saved: {image_file_name} ({'Vehicle' if is_target else 'No Vehicle'})")

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

print(f"\n✅ {saved} images processed for {target_class_name} vs No {target_class_name}.")
