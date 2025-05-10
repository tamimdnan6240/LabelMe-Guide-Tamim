import glob
from PIL import Image
import os
import shutil

# 📌 Ask user to provide the folder containing the input images
image_folder = input("📁 Enter full path to your image folder: ").strip()

# 📌 Ask user to provide the folder where LabelMe saves the .json annotation files
json_folder = input("📁 Enter full path where your LabelMe .json files are saved: ").strip()

# 📌 Ask user to provide the folder where labeled images should be saved (into subfolders by class)
output_folder = input("📁 Enter full path to save labeled images (cnn_dataset_ready): ").strip()

# 🎯 Define label shortcut keys mapped to class names
class_key_map = {
    'v': 'vehicle',
    'p': 'pedestrian',
    't': 'train',
    'e': 'empty'
}

# 📂 Create a subfolder for each class (if not already created)
for cls in class_key_map.values():
    os.makedirs(os.path.join(output_folder, cls), exist_ok=True)

# 📥 Gather all images from the image folder with supported formats
image_paths = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG']:
    image_paths.extend(glob.glob(os.path.join(image_folder, ext)))
image_paths = sorted(image_paths)

# 🔁 Loop through every image for labeling
for img_path in image_paths:
    img_name = os.path.basename(img_path)
    img_stem = os.path.splitext(img_name)[0]
    json_path = os.path.join(json_folder, img_stem + ".json")

    print(f"\n🔍 Now annotate the image in LabelMe:")
    print(f"🖼️  Image: {img_name}")
    print(f"💾 Expected .json file: {json_path}")

    # 🖼️ Preview image in system image viewer (not matplotlib)
    try:
        img = Image.open(img_path)
        img.show()
    except Exception as e:
        print(f"❌ Could not preview image {img_name}. Error: {e}")
        continue

    print("📝 Please open the image in LabelMe GUI and draw bounding boxes.")
    print("💾 Save the annotation as a .json file with the same name.")

    # ⏳ Wait until the .json file exists
    while not os.path.exists(json_path):
        input("🔁 Press ENTER after saving the .json annotation...")

    # ⌨️ Ask for the class label
    label_key = input("▶️ Enter label key [v=vehicle, p=pedestrian, t=train, e=empty]: ").lower().strip()

    if label_key in class_key_map:
        label = class_key_map[label_key]
        dst_path = os.path.join(output_folder, label, img_name)
        shutil.copy(img_path, dst_path)
        print(f"✅ Copied image to: {dst_path}")
    else:
        print(f"❌ Invalid key '{label_key}'. Skipped {img_name}.")

    print("-" * 60)
