import os
import cv2

# =====================================
# Load SFace Model
#
# SFace is a lightweight ONNX face
# recognition model (no TensorFlow
# needed) - same family as YuNet, both
# from the OpenCV Zoo.
# =====================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_recognition_sface_2021dec.onnx"
)

recognizer = cv2.FaceRecognizerSF.create(
    MODEL_PATH,
    ""
)

# Recommended threshold from the OpenCV Zoo docs for cosine similarity
COSINE_THRESHOLD = 0.363


def get_embedding(frame, face_row):
    """
    frame: full image (BGR numpy array)
    face_row: one detection row from YuNet's detect_faces()
              (bounding box + 5 landmarks + score)

    Returns a (1, 128) numpy array - the face embedding.
    """

    aligned_face = recognizer.alignCrop(frame, face_row)

    embedding = recognizer.feature(aligned_face)

    return embedding


def compare_embeddings(embedding1, embedding2):
    """
    Returns a cosine similarity score between two embeddings.
    Higher is more similar. COSINE_THRESHOLD (0.363) is the
    recommended cutoff for "same person".
    """

    score = recognizer.match(
        embedding1,
        embedding2,
        cv2.FaceRecognizerSF_FR_COSINE
    )

    return score
