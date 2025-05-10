import os
import json
import shutil
import glob

# ✅ Step 1: Set input and output paths
input_root = r"C:\Users\tadnan\Downloads\final-dataset"
output_root = os.path.join(input_root, "cnn_dataset_ready")
os.makedirs(output_root, exist_ok=True)

# ✅ Step 2: Search for all JSON files in all subfolders
json_files = glob.glob(os.path.join(input_root, "**", "*.json"), recursive=True)

print(f"🔍 Found {len(json_files)} JSON file(s).")

# ✅ Step 3: Loop through each JSON annotation
for json_path in json_files:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Skip if no shapes/annotations
        if not data.get('shapes'):
            continue

        # Get the label and image filename
        label = data['shapes'][0]['label']
        image_file = data['imagePath']

        # Locate the image path (assumes it's in the same folder as the JSON)
        image_dir = os.path.dirname(json_path)
        image_path = os.path.join(image_dir, image_file)

        if not os.path.exists(image_path):
            print(f"⚠️ Image file not found: {image_path}")
            continue

        # Create class-wise folder
        class_folder = os.path.join(output_root, label)
        os.makedirs(class_folder, exist_ok=True)

        # Copy image to the corresponding class folder
        dest_path = os.path.join(class_folder, os.path.basename(image_path))
        shutil.copy(image_path, dest_path)

    except Exception as e:
        print(f"❌ Error processing {json_path}: {e}")

print("✅ Dataset copied in ImageFolder format!")
