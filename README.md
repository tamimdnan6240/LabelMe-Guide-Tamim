# 🚦 LabelMe Annotation Guide 

This repository enables efficient image annotation for **vehicle**, **pedestrian**, **train**, and **empty crossing** classification using [LabelMe](https://github.com/wkentaro/labelme) and a custom Python script to streamline data preparation for CNN training (e.g., ResNet).

---

## ✅ 1. Environment Setup (First Time Only)

Open **Anaconda Prompt** and run the following commands to create and configure the virtual environment:

```bash
conda create -n labelme_env python=3.9 -y
conda activate labelme_env

pip install pyqt5==5.15.9
pip install labelme==5.2.1

# Annotation Workflow (Run Every Time You Label)
# Activate environment
conda activate labelme_env

# Run the image labeling script
python LabelMe_guide_Tamim.py

# (Optional) Launch the LabelMe GUI to annotate images
labelme


project_root/
├── cnn_images/                        # Images to annotate
├── Inclusion-exclusion-labels/       # LabelMe .json files (saved manually)
├── cnn_dataset_ready/                # Output folders by class
│   ├── vehicle/
│   ├── pedestrian/
│   ├── train/
│   └── empty/
├── LabelMe_guide_Tamim.py            # Python script for labeling flow

