import glob
import os
import subprocess

# Step 1: Input main folder
image_folder = input("📁 Enter full path to your MAIN image folder (with subfolders): ").strip()
json_subfolder = "jsons"

# Step 2: Define supported image formats
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tif', '*.tiff', '*.webp',
                    '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.TIF', '*.TIFF', '*.WEBP']

# Step 3: Gather all image files recursively
image_paths = []
for ext in image_extensions:
    image_paths.extend(glob.glob(os.path.join(image_folder, '**', ext), recursive=True))
image_paths = sorted(image_paths)

# Step 4: Check if any images found
if not image_paths:
    print("⚠️ No images found! Please make sure your subfolders contain supported image formats.")
    exit()

print(f"\n🔍 Found {len(image_paths)} images to annotate.")

# Step 5: Loop through and annotate
for img_path in image_paths:
    img_name = os.path.basename(img_path)
    img_stem = os.path.splitext(img_name)[0]
    img_dir = os.path.dirname(img_path)

    # Create json output directory parallel to image folder
    json_dir = os.path.join(img_dir, json_subfolder)
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, img_stem + ".json")

    # Skip already-labeled images
    if os.path.exists(json_path):
        print(f"⏩ Already annotated: {img_name}")
        continue

    # Open image in LabelMe
    print(f"\n🖼️ Labeling image: {img_path}")
    subprocess.Popen(['labelme', img_path])
    print(f"💾 Save your annotation as: {json_path}")

    # Wait for user to save annotation
    while not os.path.exists(json_path):
        input("🔁 Press ENTER after saving the .json file...")

    print(f"✅ Saved: {json_path}")
    print("------------------------------------------------------------")
