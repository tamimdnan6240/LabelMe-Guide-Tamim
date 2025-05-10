import os
import glob
import subprocess
import shutil

# ✅ Folder containing your images
image_folder = r"C:\Users\tadnan\Downloads\final-dataset"

# ✅ Try to locate labelme executable
labelme_cmd = shutil.which("labelme") or r"C:\Users\tadnan\AppData\Local\anaconda3\Scripts\labelme.exe"

if not os.path.exists(labelme_cmd):
    raise FileNotFoundError(f"❌ LabelMe not found at: {labelme_cmd}")

# ✅ Supported image types
image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tif', '*.tiff', '*.webp')

# ✅ Step 1: Collect all images using glob
all_images = []
for ext in image_extensions:
    all_images.extend(glob.glob(os.path.join(image_folder, '**', ext), recursive=True))

print(f"\n📸 Found {len(all_images)} image(s).")

# ✅ Step 2: Loop through each image and open in LabelMe
for img_path in sorted(all_images):
    img_name = os.path.basename(img_path)
    img_stem = os.path.splitext(img_name)[0]
    folder_path = os.path.dirname(img_path)
    subfolder_name = os.path.basename(folder_path)

    # Where the annotation will first be saved
    original_json = os.path.join(folder_path, img_stem + ".json")

    # Where we want to move the annotation
    json_folder = os.path.join(os.path.dirname(folder_path), f"{subfolder_name}-json")
    os.makedirs(json_folder, exist_ok=True)
    json_target = os.path.join(json_folder, img_stem + ".json")

    # Skip if already annotated
    if os.path.exists(json_target):
        print(f"⏩ Already annotated: {img_name}")
        continue

    print(f"\n🖼️ Opening LabelMe for: {img_path}")
    print("🔧 Draw → Label → Ctrl+S → Close window to continue...")

    try:
        subprocess.run(f'"{labelme_cmd}" "{img_path}"', shell=True)
    except Exception as e:
        print(f"❌ ERROR: Could not open LabelMe: {e}")
        continue

    # Move the .json file if it was saved
    if os.path.exists(original_json):
        shutil.move(original_json, json_target)
        print(f"✅ Annotation saved to: {json_target}")
    else:
        print(f"⚠️ No annotation saved for: {img_path}")
