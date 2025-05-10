🚦 LabelMe Annotation Guide – Inclusion–Exclusion Task

This guide outlines how to annotate railroad crossing images for object classification (vehicle, pedestrian, train, or empty crossing) using LabelMe and Python scripts for deep learning tasks (CNN/YOLO).

------------------------------------------------------------

✅ 1. Setup (Run Once)

conda create -n labelme_env python=3.9 -y
conda activate labelme_env
pip install pyqt5==5.15.9
pip install labelme==5.2.1
pip install -r Requirements.txt

> Ensures compatibility with LabelMe and PyQt GUI.

------------------------------------------------------------

✅ 2. Folder Structure

project_root/
├── cnn_images/                           # Input image root
│   ├── Subfolder1/                       # e.g., Day/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   ├── Subfolder2/                       # e.g., Night/
│   │   ├── img003.jpg
│   │   └── img004.jpg
├── Inclusion-exclusion-labels/          # Output LabelMe JSONs
├── annotated_images_by_label/           # Final dataset by class
│   ├── vehicle/
│   ├── pedestrian/
│   ├── train/
│   └── empty/
├── labelmeeeee-jsn-files-tamim-.py
├── jsn-to-image.py

> Input structure supports nested folders like MainFolder/Subfolder/images

------------------------------------------------------------

✅ 3. Annotation Workflow

1. Activate environment:
   conda activate labelme_env

2. Edit labelmeeeee-jsn-files-tamim-.py to set your input path:
   cnn_images/

3. Run:
   python labelmeeeee-jsn-files-tamim-.py

4. In a separate terminal, launch LabelMe:
   labelme

5. For each image:
   - Use the "Create Rectangle" tool (🔲)
   - Draw bounding boxes and label them
   - Save the .json file (same name as image)

6. Back in the terminal:
   - Press ENTER
   - Enter a class key:
     v = vehicle, p = pedestrian, t = train, e = empty

7. Run to convert JSONs to images:
   python jsn-to-image.py

Now your images are ready for CNN training. YOLO conversion requires a separate format (e.g., labelme2yolo).

------------------------------------------------------------

✅ Labeling Shortcuts

Key     Class
----    -------------
v       Vehicle
p       Pedestrian
t       Train
e       Empty

------------------------------------------------------------

❗ Troubleshooting

❌ Issue: "Nothing happens after entering folder paths"
   → Save the .json file in LabelMe and press ENTER in terminal.

❌ Issue: "Bounding boxes not visible"
   → Use the rectangle tool, not polygon.

❌ Issue: "LabelMe doesn’t launch or crashes"
   → Ensure you're in the labelme_env environment:
      conda activate labelme_env
      labelme

------------------------------------------------------------

✅ Supported Formats

- .jpg
- .jpeg
- .png
(Case-insensitive)

------------------------------------------------------------

🧠 What’s Next?

- Use annotated_images_by_label/ with torchvision.datasets.ImageFolder
- Train models like ResNet-50 or ResNet-101
- Convert to YOLO format with labelme2yolo if needed

------------------------------------------------------------

Maintained by: Tamim Adnan
Tools: Python · LabelMe · PyTorch · Matplotlib · ResNet
