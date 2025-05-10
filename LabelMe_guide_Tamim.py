# Generalized version of the script that allows multiple task folders under the main project directory
# Each task can have its own structure: e.g., inclusion-exclusion, vehicle-type, vehicle-intensity

generalized_script = '''
import glob
import os
import shutil
import subprocess
from PIL import Image

# Get base project folder (contains images in subfolders)
image_folder = input("📁 Enter full path to your MAIN image folder (with subfolders): ").strip()

# Ask for task name (e.g., inclusion-exclusion, vehicle-type, vehicle-intensity)
task_name = input("📝 Enter task name (e.g., inclusion-exclusion, vehicle-type): ").strip()

# Define root folders based on task
json_root = os.path.join(image_folder, f"{task_name}-jsons")
output_root = os.path.join(image_folder, f"{task_name}-labeled")

# Label shortcut keys
class_key_map = {
    'v': 'vehicle',
    'p': 'pedestrian',
    't': 'train',
    'e': 'empty'
}

# Recursively find all image paths
image_paths = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG']:
    image_paths.extend(glob.glob(os.path.join(image_folder, '**', ext), recursive=True))
image_paths = sorted(image_paths)

print(f"🔍 Found {len(image_paths)} images under: {image_folder}")

# Process each image
for img_path in image_paths:
    if task_name in img_path or 'json' in img_path or 'labeled' in img_path:
        continue  # Skip task-generated folders

    img_name = os.path.basename(img_path)
    img_stem = os.path.splitext(img_name)[0]
    img_dir = os.path.dirname(img_path)
    rel_path = os.path.relpath(img_dir, image_folder)

    # Setup JSON path
    json_dir = os.path.join(json_root, rel_path)
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, img_stem + ".json")

    if os.path.exists(json_path):
        print(f"⏩ Already annotated: {img_name}")
        continue

    # Launch LabelMe
    print(f"🔍 Now labeling: {img_path}")
    subprocess.Popen(['labelme', img_path])
    print(f"💾 Save annotation as: {json_path}")

    # Wait for save
    while not os.path.exists(json_path):
        input("🔁 Press ENTER after saving the .json annotation...")

    # Ask for label
    label_key = input("▶️ Enter label key [v=vehicle, p=pedestrian, t=train, e=empty]: ").lower().strip()
    if label_key not in class_key_map:
        print(f"❌ Invalid key '{label_key}'. Skipping image.")
        continue

    label = class_key_map[label_key]
    output_class_dir = os.path.join(output_root, rel_path, label)
    os.makedirs(output_class_dir, exist_ok=True)

    dst_path = os.path.join(output_class_dir, img_name)
    shutil.copy(img_path, dst_path)
    print(f"✅ Copied to: {dst_path}")
    print("------------------------------------------------------------")
'''
