
import os
import json
import glob
import re
from PIL import Image

# === CONFIGURATION ===
input_root = r"C:\Users\tadnan\Downloads\Labeled-data\Inclusion-exclusion-dataset"
output_root = os.path.join(input_root, "YOLOv8-ready")

# These subfolders should exist in input_root
class_folders = ["Vehicle", "TRAIN", "Pedestraints", "Crossing"]

# === CLEAN OUTPUT ===
for class_name in class_folders:
    os.makedirs(os.path.join(output_root, "images", class_name), exist_ok=True)
    os.makedirs(os.path.join(output_root, "labels", class_name), exist_ok=True)

# === CLASS INDEXING ===
class_map = {}
class_index = 0

def clean_label(label):
    return re.sub(r'[\\/:*?"<>|]', "_", label.strip().lower())

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

# === MAIN LOOP ===
for class_name in class_folders:
    json_files = glob.glob(os.path.join(input_root, class_name, "*.json"))
    print(f"📁 Converting {len(json_files)} annotations from '{class_name}'...")

    for json_path in json_files:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                raw = f.read().replace('T:/', '').replace('V:/', '')
            data = json.loads(raw)

            shapes = data.get("shapes", [])
            if not shapes:
                continue

            image_file = os.path.basename(data["imagePath"])
            image_path = os.path.join(os.path.dirname(json_path), image_file)
            if not os.path.exists(image_path):
                continue

            # === SAVE IMAGE ===
            img = Image.open(image_path).convert("RGB")
            w, h = img.size
            img_out_path = os.path.join(output_root, "images", class_name, image_file)
            img.save(img_out_path)

            # === SAVE LABEL ===
            label_out_path = os.path.join(output_root, "labels", class_name, image_file.replace(".jpg", ".txt").replace(".png", ".txt"))
            with open(label_out_path, "w") as out_f:
                for shape in shapes:
                    label = clean_label(shape.get("label", ""))
                    points = shape.get("points", [])
                    if not label or not points:
                        continue

                    if label not in class_map:
                        class_map[label] = class_index
                        class_index += 1
                    cls_id = class_map[label]

                    xc, yc, bw, bh = get_yolo_bbox(points, w, h)
                    out_f.write(f"{cls_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

        except Exception as e:
            print(f"❌ Error in {json_path}: {e}")

# === SAVE CLASS INDEX FILE ===
with open(os.path.join(output_root, "classes.txt"), "w") as f:
    for cls, idx in sorted(class_map.items(), key=lambda x: x[1]):
        f.write(f"{idx}: {cls}\n")

print("\n✅ Conversion complete. Images and labels organized per class.")
