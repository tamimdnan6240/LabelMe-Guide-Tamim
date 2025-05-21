import os
import cv2
import shutil
import random
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from PIL import Image

# === CONFIGURATION ===
base_dir = r"C:\Users\tadnan\Downloads\Labeled-data\Inclusion-exclusion-dataset\YOLOv8-ready"
output_dir = os.path.join(base_dir, "binary_dataset_train")
target_class = "TRAIN"
target_id = 0  # YOLO class ID for TRAIN
image_shape = (640, 640)

non_target_config = {
    "Vehicle": {"training-data": 50, "testing-data": 50},
    "Pedestrian": {"training-data": 25, "testing-data": 25},
    "Empty crossing": {"training-data": 25, "testing-data": 25}
}
target_sample_config = {
    "train": 100,
    "test": 100
}

# === STEP 1: Load and convert masks to .txt format ===
def get_image_label_pairs(class_name):
    image_dir = os.path.join(base_dir, "images", class_name)
    label_dir = os.path.join(base_dir, "labels", class_name)
    pairs = []
    for fname in os.listdir(image_dir):
        if fname.endswith(".png"):
            img_path = os.path.join(image_dir, fname)
            lbl_path = os.path.join(label_dir, fname)
            if os.path.exists(lbl_path):
                pairs.append((img_path, lbl_path))
    return pairs

def extract_yolo_boxes(mask_path, class_id=0):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    binary_mask = np.uint8(mask == class_id) * 255
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = mask.shape
    yolo_lines = []
    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        cx = (x + bw / 2) / w
        cy = (y + bh / 2) / h
        yolo_lines.append(f"{class_id} {cx:.6f} {cy:.6f} {bw / w:.6f} {bh / h:.6f}\n")
    return yolo_lines

def prepare_binary_dataset():
    for split in ['train', 'test']:
        for subfolder in ['images', 'labels']:
            os.makedirs(os.path.join(output_dir, split, subfolder), exist_ok=True)

    def copy_and_convert(pairs, split, is_target):
        for img_path, lbl_path in pairs:
            base = os.path.basename(img_path)
            img_out = os.path.join(output_dir, split, "images", base)
            lbl_out = os.path.join(output_dir, split, "labels", base.replace(".png", ".txt"))
            shutil.copy(img_path, img_out)

            if is_target:
                yolo_lines = extract_yolo_boxes(lbl_path)
                if yolo_lines:
                    with open(lbl_out, "w") as f:
                        f.writelines(yolo_lines)
            else:
                open(lbl_out, "w").close()

    train_pairs = get_image_label_pairs("TRAIN")
    for split in ["train", "test"]:
        copy_and_convert(random.sample(train_pairs, target_sample_config[split]), split, True)

    for cls in non_target_config:
        cls_pairs = get_image_label_pairs(cls)
        for split in ["train", "test"]:
            sample = random.sample(cls_pairs, non_target_config[cls][f"{split}ing-data"])
            copy_and_convert(sample, split, False)

prepare_binary_dataset()
print("✅ Dataset prepared.")

# === STEP 2: Create data.yaml
yaml_path = os.path.join(output_dir, "train.yaml")
with open(yaml_path, "w") as f:
    f.write(f"""path: {output_dir}
train: train/images
val: train/images
names:
  0: {target_class}
""")

# === STEP 3: Train
model = YOLO("yolov8s.pt")
model.train(data=yaml_path, epochs=10, imgsz=640, batch=16, name="yolov8_train_binary", project="runs/train", patience=5, device="cpu")

# === STEP 4: Evaluate
model_path = "runs/train/yolov8_train_binary/weights/best.pt"
model = YOLO(model_path)
test_images_dir = os.path.join(output_dir, "test", "images")
test_images = [os.path.join(test_images_dir, f) for f in os.listdir(test_images_dir) if f.endswith(".png")]
results = model(test_images)

true_labels, pred_labels = [], []
for r in results:
    for b in r.boxes:
        pred_labels.append(int(b.cls[0].item()))
    for path in r.path:
        lbl_file = path.replace("\\images\\", "\\labels\\").replace(".png", ".txt")
        if os.path.exists(lbl_file):
            with open(lbl_file, "r") as f:
                true_labels += [int(line.split()[0]) for line in f.readlines()]

print("\n📋 Classification Report:")
print(classification_report(true_labels, pred_labels, target_names=[f"No {target_class}", target_class]))

cm = confusion_matrix(true_labels, pred_labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[f"No {target_class}", target_class])
disp.plot(cmap=plt.cm.Blues)
plt.title(f"Confusion Matrix - YOLOv8 {target_class}")
plt.show()
