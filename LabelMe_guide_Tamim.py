import glob
from PIL import Image
import matplotlib.pyplot as plt
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

# 🔤 Sort the image list for consistent processing order
image_paths = sorted(image_paths)

# 🔁 Loop through every image for labeling
for img_path in image_paths:
    # 🧾 Get the filename and its stem (without extension)
    img_name = os.path.basename(img_path)
    img_stem = os.path.splitext(img_name)[0]

    # 📄 Build the expected .json path where LabelMe will save the annotation
    json_path = os.path.join(json_folder, img_stem + ".json")

    try:
        # 🖼️ Open and display the image using matplotlib
        img = Image.open(img_path)
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Now annotate and then label:\n{img_name}")
        plt.show()
    except Exception as e:
        # ❌ Skip the image if it fails to load
        print(f"❌ Failed to load image {img_name}. Skipping. Error: {e}")
        continue

    # 🔔 Remind the user to annotate the image using LabelMe GUI
    print(f"📝 Annotate this image using LabelMe GUI.")
    print(f"💾 Save the .json file as: {json_path}")

    # ⏳ Wait until the corresponding .json file appears (i.e., annotation is saved)
    while not os.path.exists(json_path):
        input("🔁 Press ENTER after saving the .json annotation...")

    # ⌨️ Ask the user to classify the image using a keyboard shortcut
    label_key = input("▶️ Enter label key [v=vehicle, p=pedestrian, t=train, e=empty]: ").lower().strip()

    # ✅ If the pressed key is valid, copy the image to its class folder
    if label_key in class_key_map:
        label = class_key_map[label_key]
        dst_path = os.path.join(output_folder, label, img_name)
        shutil.copy(img_path, dst_path)
        print(f"✅ Copied image to: {dst_path}\n{'-'*60}")
    else:
        # ❗ Warn the user and skip the image if the key is invalid
        print(f"❌ Invalid key '{label_key}'. Skipped {img_name}.\n{'-'*60}")
