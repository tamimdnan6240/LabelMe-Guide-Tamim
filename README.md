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
│  
├── cnn_images/                          ← Input image root directory  
│   ├── Day/                             ← Subfolder 1 (e.g., daytime images)  
│   │   ├── image_001.jpg  
│   │   ├── image_002.jpg  
│   │   └── ...  
│   ├── Night/                           ← Subfolder 2 (e.g., nighttime images)  
│   │   ├── image_003.jpg  
│   │   ├── image_004.jpg  
│   │   └── ...  
│  
├── Inclusion-exclusion-labels/         ← Output folder for saved LabelMe .json files  
│  
├── annotated_images_by_label/          ← Final dataset organized by class  
│   ├── vehicle/  
│   ├── pedestrian/  
│   ├── train/  
│   └── empty/  
│  
├── labelmeeeee-jsn-files-tamim-.py     ← Script for annotation workflow  
├── jsn-to-image.py                     ← Script to convert JSONs to annotated images  

> Nested folders inside cnn_images/ are supported.

------------------------------------------------------------

✅ 3. Annotation Workflow
This workflow is the same for each tasks. Use the same method for all tasks. 

1. Activate environment:  
   conda activate labelme_env  

2. Edit `labelmeeeee-inclusion-exclusion-tamim-.py` to point to the input image folder (r"C:\Users\tadnan\Downloads\Labeled-data\Inclusion-exclusion-dataset")  

3. Run:  
   python labelmeeeee-inclusion-exclusion-tamim-.py  

4. In a second terminal, launch LabelMe will open one by one images 

5. Inside LabelMe:  
   - Use the "Create Rectangle" tool (🔲)  
   - Draw bounding boxes and label each object  
   - Save the `.json` file (same name as image - images and corresponding json should palced pairwisely.  

6. In the script terminal:  
   - Press `ENTER`  
   - Enter label key:  
     V = vehicle, P = pedestrian, T = train, E = empty  

7. Convert saved JSONs into cropped images:  
   python jsn-to-image-inclusion-exclusion.py 

Your dataset is now ready for CNN training. For YOLO, convert JSONs using `labelme2yolo`.

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

❌ "Nothing happens after entering folder paths"  
→ Make sure you've saved a `.json` file in LabelMe, then press ENTER.  

❌ "Bounding boxes are not visible"  
→ Use the rectangle tool instead of polygon.  

❌ "LabelMe doesn’t launch or crashes"  
→ Make sure your conda environment is activated:  
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

- Use `annotated_images_by_label/` with `torchvision.datasets.ImageFolder`  
- Train models like ResNet-50, ResNet-101  
- For YOLO, convert using LabelMe to YOLO tools like `labelme2yolo`

------------------------------------------------------------

Maintained by: Tamim Adnan  
Tools: Python · LabelMe · PyTorch · Matplotlib · ResNet  
