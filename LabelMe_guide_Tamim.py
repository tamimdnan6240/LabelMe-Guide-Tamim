import glob
import os
import shutil
import subprocess
from PIL import Image

# 📁 Input directories
image_folder = input("📁 Enter full path to your MAIN image folder (with subfolders): ").strip()
json_folder = input("📁 Enter full path where your LabelMe .json files will be saved: ").strip()
output_folder = input("📁 Enter full path to save labeled images (cnn_dataset_ready): ").strip()

# 🔠 Class shortcut map
class_key_map = {
    'v': 'vehicle',
    'p': 'pedestrian',
    't': 'train',
    'e': 'empty'
}

# 📁 Create class folders
for cls in class_key_map.values():
    os.makedirs(os.path.join(output_folder, cls), exist_ok=True)

# 📷 Recursively find images in all subdirectories
image_paths = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG']:
    image_paths.extend(glob.glob(os.path.join(image_folder, '**', ext), recursive=True))
image_paths = sorted(image_paths)

print(f"🔍 Found {len(image_paths)} images in {image_folder}")

# 🔁 Loop through each image
for img_path in image_paths:
    img_name = os.path.basename(img_path)
    img_stem = os.path.splitext(img_name)[0]
    json_path = os.path.join(json_folder, img_stem + ".json")

    # 🔁 Skip if .json already exists
    if os.path.exists(json_path):
        print(f"⏩ Already annotated: {img_name}")
        continue

    # 🖼️ Open LabelMe with this image
    print(f"\n🔍 Now labeling: {img_name}")
    print(f"📂 Opening in LabelMe GUI...")
    subprocess.Popen(['labelme', img_path])

    print(f"💾 Please save the annotation as: {json_path}")

    # Wait until .json is created
    while not os.path.exists(json_path):
        input("🔁 Press ENTER once you have saved the .json annotation in LabelMe...")

    # Ask for class assignment
    label_key = input("▶️ Enter label key [v=vehicle, p=pedestrian, t=train, e=empty]: ").lower().strip()

    if label_key in class_key_map:
        label = class_key_map[label_key]
        dst_path = os.path.join(output_folder, label, img_name)
        shutil.copy(img_path, dst_path)
        print(f"✅ Copied to: {dst_path}")
    else:
        print(f"❌ Invalid key '{label_key}'. Skipped {img_name}.")

    print("------------------------------------------------------------")
