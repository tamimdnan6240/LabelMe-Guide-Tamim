# Final clean version of the README saved as .txt with proper spacing

readme_txt = """
🚦 LabelMe Annotation Guide – Inclusion–Exclusion Task (by Tamim)

This repository enables efficient image annotation for vehicle, pedestrian, train, and empty crossing classification using LabelMe and a custom Python script (LabelMe_guide_Tamim.py) to organize images into class folders for CNN training (e.g., ResNet).

------------------------------------------------------------

✅ 1. Environment Setup (Run Only Once)

Use Anaconda Prompt to create a clean environment and install the required tools:

conda create -n labelme_env python=3.9 -y

conda activate labelme_env

pip install pyqt5==5.15.9

pip install labelme==5.2.1

✅ This avoids common plugin and GUI issues that occur with newer versions of LabelMe or PyQt.

------------------------------------------------------------

✅ 2. Project Structure

Your project folder should look like this:

project_root/
├── cnn_images/                        # Input images to annotate
├── Inclusion-exclusion-labels/       # Output LabelMe .json files

├── cnn_dataset_ready/                # Final labeled dataset sorted by class
│   ├── vehicle/
│   ├── pedestrian/
│   ├── train/
│   └── empty/

├── LabelMe_guide_Tamim.py            # Custom Python script for annotation workflow

------------------------------------------------------------

✅ 3. Labeling Workflow (Run Every Time You Annotate)

conda activate labelme_env
python LabelMe_guide_Tamim.py
labelme   # (Optional: open in another terminal)

------------------------------------------------------------

🛠️ Step-by-Step Annotation Instructions

1. The script asks for:
   - Image folder (e.g., cnn_images)
   - LabelMe JSON folder (e.g., Inclusion-exclusion-labels)
   - Output folder (e.g., cnn_dataset_ready)

2. It shows one image using matplotlib.

3. In a second terminal, run:
   labelme

4. Inside LabelMe GUI:
   - Use the "Create Rectangle" tool (🔲)
   - Draw bounding boxes, label each object
   - Save the .json file to Inclusion-exclusion-labels/
   - File name must match the image (e.g., car1.jpg → car1.json)

5. Return to the terminal, press ENTER

6. Enter label key:
   ▶️ [v=vehicle, p=pedestrian, t=train, e=empty]

7. The image is copied to the appropriate class folder.

Repeat for each image.

------------------------------------------------------------

✅ Labeling Shortcuts

Key     Class
----    -------------
v       Vehicle
p       Pedestrian
t       Train
e       Empty Cross

------------------------------------------------------------

❗ Issues You May Face & Fixes

❌ Issue: "Nothing happens after entering folder paths"
Reason: Script waits for annotation (.json) to be saved
Fix: Open LabelMe → Draw bounding boxes → Save .json → Press ENTER

❌ Issue: "Bounding boxes are not visible"
Reason: You used the polygon tool
Fix: Use "Create Rectangle" tool in LabelMe (🔲)

❌ Issue: "LabelMe doesn't launch or crashes"
Fix: Run with virtual environment activated:
conda activate labelme_env
labelme

------------------------------------------------------------

✅ Supported Image Formats

- .jpg
- .jpeg
- .png
- Case-insensitive: .JPG, .PNG

------------------------------------------------------------

💡 Tips for Smooth Annotation

- Keep LabelMe GUI open throughout your session
- Ensure .json filename matches the image
- Label assignment is handled via keyboard shortcuts

------------------------------------------------------------

🧠 What's Next?

- Your dataset is now organized in cnn_dataset_ready/
- Ready to use with torchvision.datasets.ImageFolder
- You can now:
  - Train ResNet50/101
  - Evaluate classification models
  - Convert to YOLO format using labelme2yolo if needed

------------------------------------------------------------

Maintained by: Tamim Adnan
Toolset: Python · LabelMe · PyTorch · Matplotlib · ResNet
"""
