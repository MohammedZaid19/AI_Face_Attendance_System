import cv2
import json
import mysql.connector
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

from attendance_utils import mark_attendance
from models.yunet_detector import detect_faces


# =====================================
# Database Connection
# =====================================

def connect_database():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="zaid08",
        database="ai_face_attendance"
    )


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

    if best_score > 0.60:

        return best_student, best_score

    return None, best_score


# =====================================
# Attendance
# =====================================

def start_attendance():

    students = load_embeddings()

    if len(students) == 0:

        print("No Registered Students")
        return

    cap = cv2.VideoCapture(0)

    print("\nAttendance Started")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        faces = detect_faces(frame)

        if faces is not None:

            for face in faces:

                x, y, w, h = face[:4].astype(int)

                crop = frame[y:y+h, x:x+w]

                try:

                    student, score = recognize_student(
                        crop,
                        students
                    )

                    if student is not None:

                        color = (0,255,0)

                        label = f"{student['student_name']} ({score:.2f})"

                        mark_attendance(
                            student["student_id"],
                            "Present"
                        )

                    else:

                        color = (0,0,255)

                        label = "Unknown"

                except Exception:

                    color = (0,0,255)

                    label = "Unknown"

                cv2.rectangle(
                    frame,
                    (x,y),
                    (x+w,y+h),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

        cv2.putText(
            frame,
            "Press Q to Exit",
            (20,30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

        cv2.imshow(
            "AI Face Attendance",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()


# =====================================

if __name__ == "__main__":

    start_attendance()