import os
import cv2
import time
from ultralytics import YOLO

# =====================================
# Load YOLOv11 Model
# =====================================

model = YOLO("yolo11n.pt")

# =====================================
# Dataset Path
# =====================================

dataset_path = r"C:\Users\Mohammed Zaid Khalid\fiftyone\open-images-v7\validation\data"

images = [
    f for f in os.listdir(dataset_path)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

print("=" * 50)
print("YOLOv11 Face Detection")
print("=" * 50)
print("Total Images :", len(images))
print()

total_time = 0
processed = 0

# =====================================
# Process Images
# =====================================

for image_name in images:

    image_path = os.path.join(dataset_path, image_name)

    image = cv2.imread(image_path)

    if image is None:
        continue

    start = time.time()

    results = model(image)

    end = time.time()

    total_time += (end - start)
    processed += 1

    annotated = results[0].plot()

    cv2.imshow("YOLOv11 Detection", annotated)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cv2.destroyAllWindows()

# =====================================
# Results
# =====================================

print("\nFinished")

print("Images Processed :", processed)

avg_time = total_time / processed

print(f"Average Detection Time : {avg_time:.4f} sec")

print(f"FPS : {1/avg_time:.2f}")