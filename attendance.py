import json
import cv2
import numpy as np

from attendance_utils import mark_attendance
from models.yunet_detector import detect_faces
from models.sface_recognizer import get_embedding, compare_embeddings, COSINE_THRESHOLD
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

        embedding_array = np.array(
            json.loads(student["embedding"]),
            dtype=np.float32
        )

        # SFace expects a (1, 128) shaped array
        student["embedding"] = embedding_array.reshape(1, -1)

    return students


# =====================================
# Recognize Student
#
# Returns: (student_or_None, best_score, debug_message)
# =====================================

def recognize_student(frame, face_row, students):

    query_embedding = get_embedding(frame, face_row)

    best_score = -1
    best_student = None

    for student in students:

        score = compare_embeddings(
            query_embedding,
            student["embedding"]
        )

        if score > best_score:

            best_score = score
            best_student = student

    debug_message = (
        f"Best match: "
        f"{best_student['student_name'] if best_student else 'None'} "
        f"| score={best_score:.4f} "
        f"| threshold={COSINE_THRESHOLD}"
    )

    if best_score > COSINE_THRESHOLD:

        return best_student, best_score, debug_message

    return None, best_score, debug_message


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
#   debug_messages - list of strings with
#             score info / errors, shown
#             on screen for troubleshooting
# =====================================

def process_attendance_frame(frame):

    students = load_embeddings()

    results = []
    debug_messages = []

    if len(students) == 0:

        debug_messages.append(
            "No registered students found in the database at all."
        )

        return frame, results, debug_messages

    faces = detect_faces(frame)

    if faces is None or len(faces) == 0:

        debug_messages.append(
            "YuNet did not detect any face in this photo."
        )

        return frame, results, debug_messages

    for face_row in faces:

        x, y, w, h = face_row[:4].astype(int)

        x, y = max(x, 0), max(y, 0)

        try:

            student, score, debug_message = recognize_student(
                frame,
                face_row,
                students
            )

            debug_messages.append(debug_message)

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

        except Exception as e:

            debug_messages.append(f"Recognition Error: {e}")

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

    return frame, results, debug_messages
