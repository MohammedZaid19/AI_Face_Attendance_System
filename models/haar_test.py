import os
import cv2
import time

# =====================================
# Haar Cascade Model
# =====================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(cascade_path)

if face_detector.empty():
    print("❌ Failed to load Haar Cascade!")
    exit()

print("✅ Haar Cascade Loaded Successfully!")

# =====================================
# Dataset Path
# =====================================

dataset_path = r"C:\Users\Mohammed Zaid Khalid\fiftyone\open-images-v7\validation\data"

if not os.path.exists(dataset_path):
    print("❌ Dataset folder not found!")
    exit()

images = [
    f for f in os.listdir(dataset_path)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

print("=" * 50)
print("Haar Cascade Face Detection")
print("=" * 50)
print("Total Images :", len(images))

# =====================================
# Output Folder
# =====================================

output_dir = os.path.join(BASE_DIR, "results_haar")
os.makedirs(output_dir, exist_ok=True)

total_faces = 0
total_time = 0
processed = 0

# =====================================
# Detection
# =====================================

for image_name in images:

    image_path = os.path.join(dataset_path, image_name)

    image = cv2.imread(image_path)

    if image is None:
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    start = time.time()

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    end = time.time()

    total_time += (end - start)
    processed += 1
    total_faces += len(faces)

    for (x, y, w, h) in faces:

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imwrite(
        os.path.join(output_dir, image_name),
        image
    )

# =====================================
# Results
# =====================================

print("\nFinished")
print("Images Processed :", processed)
print("Faces Detected   :", total_faces)

if processed > 0:
    avg = total_time / processed
    fps = 1 / avg

    print(f"Average Detection Time : {avg:.4f} sec")
    print(f"FPS                    : {fps:.2f}")

print("\nResults Saved In :", output_dir)