import json
import cv2
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

from attendance_utils import mark_attendance
from models.yunet_detector import detect_faces
from db import connect_database


# =====================================
# Load Stored Embeddings
# =====================================

def load_embeddings():

    connection = connect_database()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        s.student_id,
        s.student_name,
        s.roll_number,
        f.embedding
    FROM students s
    JOIN face_embeddings f
    ON s.student_id=f.student_id
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    for student in students:

        student["embedding"] = np.array(
            json.loads(student["embedding"])
        )

    return students


# =====================================
# Generate Embedding
# =====================================

def generate_embedding(face):

    embedding = DeepFace.represent(
        img_path=face,
        model_name="ArcFace",
        detector_backend="skip",
        enforce_detection=False
    )

    return np.array(
        embedding[0]["embedding"]
    )


# =====================================
# Recognize Student
# =====================================

def recognize_student(face, students):

    query_embedding = generate_embedding(face)

    best_score = -1
    best_student = None

    for student in students:

        score = cosine_similarity(
            [query_embedding],
            [student["embedding"]]
        )[0][0]

        if score > best_score:

            best_score = score
            best_student = student

    if best_score > 0.70:

        return best_student, best_score

    return None, best_score


# =====================================
# Process A Single Captured Photo
#
# frame: numpy array (BGR) - one image
# already captured by the browser camera
# (st.camera_input), not a live feed.
#
# Returns:
#   annotated_frame - frame with boxes/
#                      labels drawn on it
#   results - list of dicts describing
#             what was recognized/marked
# =====================================

def process_attendance_frame(frame):

    students = load_embeddings()

    results = []

    if len(students) == 0:
        return frame, results

    faces = detect_faces(frame)

    if faces is not None:

        for face in faces:

            x, y, w, h = face[:4].astype(int)

            x, y = max(x, 0), max(y, 0)

            crop = frame[y:y+h, x:x+w]

            if crop.size == 0:
                continue

            try:

                student, score = recognize_student(
                    crop,
                    students
                )

                if student is not None:

                    color = (0, 255, 0)

                    label = f"{student['student_name']} ({score:.2f})"

                    marked = mark_attendance(
                        student["student_id"],
                        "Present"
                    )

                    results.append({
                        "name": student["student_name"],
                        "roll_number": student["roll_number"],
                        "score": float(score),
                        "marked": marked
                    })

                else:

                    color = (0, 0, 255)

                    label = "Unknown"

            except Exception:

                color = (0, 0, 255)

                label = "Unknown"

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                color,
                2
            )

            cv2.putText(
                frame,
                label,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    return frame, results
