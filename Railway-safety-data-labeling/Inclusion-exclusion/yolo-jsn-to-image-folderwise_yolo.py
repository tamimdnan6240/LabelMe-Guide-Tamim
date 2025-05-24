import os
import json
import glob
import re
from PIL import Image, ImageDraw
import numpy as np

# === CONFIGURATION ===
input_root = r"C:\Users\tadnan\Downloads\Labeled-data\Inclusion-json-exclusion-dataset"
output_root = os.path.join(input_root, "YOLOv8-ready-inclusion-exclusion")
label_format = "txt"  # Change to "png" if you want label masks instead

# Folder-to-cleaned-class mapping
class_folders = {
    "Vehicle": "Vehicle",
    "TRAIN": "Train",
    "Pedestraints": "Pedestrian",
    "Crossing": "Empty crossing"
}

# === SETUP OUTPUT STRUCTURE ===
for folder, class_name in class_folders.items():
    os.makedirs(os.path.join(output_root, "images", class_name), exist_ok=True)
    os.makedirs(os.path.join(output_root, "labels", class_name), exist_ok=True)

# === YOLO BBOX UTILITY ===
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
class_map = {}
class_index = 0

for folder_name, class_name in class_folders.items():
    json_files = glob.glob(os.path.join(input_root, folder_name, "*.json"))
    print(f"📁 Converting {len(json_files)} annotations from '{folder_name}' → '{class_name}'")

    for json_path in json_files:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                raw = f.read().replace("T:/", "").replace("V:/", "")
            data = json.loads(raw)

            shapes = data.get("shapes", [])
            if not shapes:
                continue

            image_file = os.path.basename(data["imagePath"])
            image_path = os.path.join(os.path.dirname(json_path), image_file)
            if not os.path.exists(image_path):
                continue

            # === Load and Save Image ===
            img = Image.open(image_path).convert("RGB")
            w, h = img.size
            img_out = os.path.join(output_root, "images", class_name, image_file)
            img.save(img_out)

            # === Generate Label ===
            if label_format == "txt":
                label_file = image_file.rsplit(".", 1)[0] + ".txt"
                label_out = os.path.join(output_root, "labels", class_name, label_file)
                with open(label_out, "w") as out_f:
                    for shape in shapes:
                        raw_label = shape.get("label", "")
                        cleaned = re.sub(r'[\\/:*?"<>|]', "_", raw_label.strip())
                        label = cleaned.capitalize()
                        points = shape.get("points", [])
                        if not label or not points:
                            continue

                        if label not in class_map:
                            class_map[label] = class_index
                            class_index += 1
                        cls_id = class_map[label]

                        x, y, bw, bh = get_yolo_bbox(points, w, h)
                        out_f.write(f"{cls_id} {x:.6f} {y:.6f} {bw:.6f} {bh:.6f}\n")
            elif label_format == "png":
                label_mask = Image.new("L", (w, h), 0)
                draw = ImageDraw.Draw(label_mask)
                for shape in shapes:
                    raw_label = shape.get("label", "")
                    cleaned = re.sub(r'[\\/:*?"<>|]', "_", raw_label.strip())
                    label = cleaned.capitalize()
                    points = shape.get("points", [])
                    if not label or not points:
                        continue

                    if label not in class_map:
                        class_map[label] = class_index
                        class_index += 1
                    cls_id = class_map[label]

                    polygon = [(float(x), float(y)) for x, y in points]
                    draw.polygon(polygon, fill=cls_id)
                label_file = image_file.rsplit(".", 1)[0] + ".png"
                label_out = os.path.join(output_root, "labels", class_name, label_file)
                label_mask.save(label_out)

        except Exception as e:
            print(f"❌ Error processing {json_path}: {e}")

# === SAVE CLASS INDEX MAP ===
with open(os.path.join(output_root, "classes.txt"), "w") as f:
    for cls, idx in sorted(class_map.items(), key=lambda x: x[1]):
        f.write(f"{idx}: {cls}\n")

print("\n✅ Conversion complete. YOLO-ready images and labels saved by class.")
