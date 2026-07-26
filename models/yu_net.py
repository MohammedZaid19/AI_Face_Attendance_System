# import os
# import cv2
# import time
#
# # =====================================
# # YuNet Model
# # =====================================
#
# model_path = "models/face_detection_yunet_2023mar.onnx"
#
# detector = cv2.FaceDetectorYN.create(
#     model=model_path,
#     config="",
#     input_size=(320, 320),
#     score_threshold=0.8,
#     nms_threshold=0.3,
#     top_k=5000
# )
#
# # =====================================
# # Dataset Path
# # =====================================
#
# dataset_path = r"C:\Users\Mohammed Zaid Khalid\fiftyone\open-images-v7\validation\data"
#
# images = [
#     f for f in os.listdir(dataset_path)
#     if f.lower().endswith((".jpg", ".jpeg", ".png"))
# ]
#
# print("=" * 50)
# print("YuNet Face Detection")
# print("=" * 50)
# print("Total Images :", len(images))
#
# total_faces = 0
# total_time = 0
# processed = 0
#
# output_dir = "results_yunet"
# os.makedirs(output_dir, exist_ok=True)
#
# # =====================================
# # Detection
# # =====================================
#
# for image_name in images:
#
#     image_path = os.path.join(dataset_path, image_name)
#
#     image = cv2.imread(image_path)
#
#     if image is None:
#         continue
#
#     h, w = image.shape[:2]
#
#     detector.setInputSize((w, h))
#
#     start = time.time()
#
#     _, faces = detector.detect(image)
#
#     end = time.time()
#
#     total_time += end - start
#     processed += 1
#
#     if faces is not None:
#
#         total_faces += len(faces)
#
#         for face in faces:
#
#             x, y, fw, fh = face[:4].astype(int)
#
#             cv2.rectangle(
#                 image,
#                 (x, y),
#                 (x + fw, y + fh),
#                 (0, 255, 0),
#                 2
#             )
#
#     cv2.imwrite(
#         os.path.join(output_dir, image_name),
#         image
#     )
#
# # =====================================
# # Results
# # =====================================
#
# print("\nFinished")
# print("Images Processed :", processed)
# print("Faces Detected :", total_faces)
#
# avg = total_time / processed
#
# print(f"Average Detection Time : {avg:.4f} sec")
# print(f"FPS : {1/avg:.2f}")
import os
import cv2
import time

# =====================================
# Project Base Directory
# =====================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =====================================
# YuNet Model Path
# =====================================

model_path = os.path.join(
    BASE_DIR,
    "models",
    "face_detection_yunet_2023mar.onnx"
)

print("Model Path :", model_path)

if not os.path.exists(model_path):
    print("❌ YuNet model not found!")
    exit()

# =====================================
# Load YuNet Model
# =====================================

detector = cv2.FaceDetectorYN.create(
    model=model_path,
    config="",
    input_size=(320, 320),
    score_threshold=0.8,
    nms_threshold=0.3,
    top_k=5000
)

print("✅ YuNet Model Loaded Successfully!")

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

print("\n" + "=" * 50)
print("YuNet Face Detection")
print("=" * 50)
print("Total Images :", len(images))

total_faces = 0
total_time = 0
processed = 0

# =====================================
# Output Folder
# =====================================

output_dir = os.path.join(BASE_DIR, "results_yunet")
os.makedirs(output_dir, exist_ok=True)

# =====================================
# Detection
# =====================================

for image_name in images:

    image_path = os.path.join(dataset_path, image_name)

    image = cv2.imread(image_path)

    if image is None:
        continue

    h, w = image.shape[:2]

    detector.setInputSize((w, h))

    start = time.time()

    _, faces = detector.detect(image)

    end = time.time()

    total_time += (end - start)
    processed += 1

    if faces is not None:

        total_faces += len(faces)

        for face in faces:

            x, y, fw, fh = face[:4].astype(int)

            cv2.rectangle(
                image,
                (x, y),
                (x + fw, y + fh),
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

    print(f"Average Detection Time : {avg:.4f} sec")
    print(f"FPS                    : {1 / avg:.2f}")

print("\nResults Saved In :", output_dir)