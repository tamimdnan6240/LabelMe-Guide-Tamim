import os
import json
import glob

# 🔧 Update this to your dataset root
input_root = r"C:\Users\tadnan\Downloads\final-dataset"

# 🔍 Find all .json files
json_files = glob.glob(os.path.join(input_root, '**', '*.json'), recursive=True)
print(f"🔍 Found {len(json_files)} JSON file(s) to clean.")

fixed_count = 0

for json_path in json_files:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Fix imagePath to be filename only
        original_path = data.get('imagePath', '')
        fixed_filename = os.path.basename(original_path)
        data['imagePath'] = fixed_filename

        # Overwrite the same JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        fixed_count += 1

    except Exception as e:
        print(f"❌ Failed to clean {json_path}: {e}")

print(f"✅ Cleaned {fixed_count} JSON file(s). Now all 'imagePath' entries use only filenames.")
