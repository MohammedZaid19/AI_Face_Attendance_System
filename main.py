# import os
# import cv2
# import json
# import mysql.connector
# from deepface import DeepFace
#
#
# # =====================================
# # Database Connection
# # =====================================
#
# def connect_database():
#
#     try:
#
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="zaid08",
#             database="ai_face_attendance"
#         )
#
#         return connection
#
#     except mysql.connector.Error as e:
#
#         print("❌ Database Error :", e)
#         return None
#
#
# # =====================================
# # Capture Face
# # =====================================
#
# def capture_face(roll_number):
#
#     if not os.path.exists("images"):
#         os.makedirs("images")
#
#     cap = cv2.VideoCapture(0)
#
#     if not cap.isOpened():
#
#         print("❌ Cannot Open Webcam")
#         return None
#
#     print("\n===================================")
#     print("Press 'S' to Save Face")
#     print("Press 'Q' to Cancel")
#     print("===================================\n")
#
#     image_path = f"images/{roll_number}.jpg"
#
#     while True:
#
#         ret, frame = cap.read()
#
#         if not ret:
#             break
#
#         cv2.imshow("Capture Face", frame)
#
#         key = cv2.waitKey(1) & 0xFF
#
#         if key == ord("s"):
#
#             cv2.imwrite(image_path, frame)
#
#             print(f"✅ Image Saved : {image_path}")
#
#             break
#
#         elif key == ord("q"):
#
#             image_path = None
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#     return image_path
#
#
# # =====================================
# # Generate ArcFace Embedding
# # =====================================
#
# def generate_embedding(image_path):
#
#     embedding = DeepFace.represent(
#         img_path=image_path,
#         model_name="ArcFace",
#         detector_backend="skip",
#         enforce_detection=False
#     )
#
#     return embedding[0]["embedding"]
#
#
# # =====================================
# # Register Student
# # =====================================
#
# def register_student(student_name,
#                      roll_number,
#                      department):
#
#     connection = connect_database()
#
#     if connection is None:
#         return False
#
#     cursor = connection.cursor()
#
#     # ----------------------------
#     # Capture Face
#     # ----------------------------
#
#     image_path = capture_face(roll_number)
#
#     if image_path is None:
#
#         cursor.close()
#         connection.close()
#
#         return False
#
#     # ----------------------------
#     # Generate ArcFace Embedding
#     # ----------------------------
#
#     try:
#
#         embedding = generate_embedding(image_path)
#
#     except Exception as e:
#
#         print("Embedding Error :", e)
#
#         cursor.close()
#         connection.close()
#
#         return False
#
#     # ----------------------------
#     # Save Student
#     # ----------------------------
#
#     student_query = """
#     INSERT INTO students
#     (
#         student_name,
#         roll_number,
#         department,
#         image_path
#     )
#     VALUES
#     (
#         %s,
#         %s,
#         %s,
#         %s
#     )
#     """
#
#     student_values = (
#         student_name,
#         roll_number,
#         department,
#         image_path
#     )
#
#     try:
#
#         cursor.execute(student_query, student_values)
#
#         student_id = cursor.lastrowid
#
#         embedding_query = """
#         INSERT INTO face_embeddings
#         (
#             student_id,
#             embedding
#         )
#         VALUES
#         (
#             %s,
#             %s
#         )
#         """
#
#         cursor.execute(
#             embedding_query,
#             (
#                 student_id,
#                 json.dumps(embedding)
#             )
#         )
#
#         connection.commit()
#
#         print("\n===================================")
#         print("✅ Student Registered Successfully")
#         print("✅ Face Image Saved")
#         print("✅ ArcFace Embedding Generated")
#         print("✅ Embedding Stored in MySQL")
#         print("===================================")
#
#         return True
#
#     except mysql.connector.Error as e:
#
#         print("Database Error :", e)
#
#         return False
#
#     finally:
#
#         cursor.close()
#         connection.close()
#
#
# # =====================================
# # Terminal Testing
# # =====================================
#
# if __name__ == "__main__":
#
#     print("========== Student Registration ==========")
#
#     student_name = input("Student Name : ")
#     roll_number = input("Roll Number  : ")
#     department = input("Department   : ")
#
#     register_student(
#         student_name,
#         roll_number,
#         department
#     )
import os
import cv2
import json
import mysql.connector
from deepface import DeepFace

from db import connect_database as _connect_database


# =====================================
# Database Connection (wrapped to keep
# the original None-on-failure behavior
# used throughout this file)
# =====================================

def connect_database():

    try:

        return _connect_database()

    except mysql.connector.Error as e:

        print("❌ Database Error :", e)
        return None


# =====================================
# Capture Face
# =====================================

def capture_face(roll_number):

    if not os.path.exists("images"):
        os.makedirs("images")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("❌ Cannot Open Webcam")
        return None

    print("\n===================================")
    print("Press 'S' to Save Face")
    print("Press 'Q' to Cancel")
    print("===================================\n")

    image_path = f"images/{roll_number}.jpg"

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Capture Face", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):

            cv2.imwrite(image_path, frame)

            print(f"✅ Image Saved : {image_path}")

            break

        elif key == ord("q"):

            image_path = None
            break

    cap.release()
    cv2.destroyAllWindows()

    return image_path


# =====================================
# Generate ArcFace Embedding
# =====================================

def generate_embedding(image_path):

    embedding = DeepFace.represent(
        img_path=image_path,
        model_name="ArcFace",
        detector_backend="skip",
        enforce_detection=False
    )

    return embedding[0]["embedding"]


# =====================================
# Register Student
# =====================================

def register_student(student_name,
                     roll_number,
                     department):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    # ----------------------------
    # Capture Face
    # ----------------------------

    image_path = capture_face(roll_number)

    if image_path is None:

        cursor.close()
        connection.close()

        return False

    # ----------------------------
    # Generate ArcFace Embedding
    # ----------------------------

    try:

        embedding = generate_embedding(image_path)

    except Exception as e:

        print("Embedding Error :", e)

        cursor.close()
        connection.close()

        return False

    # ----------------------------
    # Save Student
    # ----------------------------

    student_query = """
    INSERT INTO students
    (
        student_name,
        roll_number,
        department,
        image_path
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    )
    """

    student_values = (
        student_name,
        roll_number,
        department,
        image_path
    )

    try:

        cursor.execute(student_query, student_values)

        student_id = cursor.lastrowid

        embedding_query = """
        INSERT INTO face_embeddings
        (
            student_id,
            embedding
        )
        VALUES
        (
            %s,
            %s
        )
        """

        cursor.execute(
            embedding_query,
            (
                student_id,
                json.dumps(embedding)
            )
        )

        connection.commit()

        print("\n===================================")
        print("✅ Student Registered Successfully")
        print("✅ Face Image Saved")
        print("✅ ArcFace Embedding Generated")
        print("✅ Embedding Stored in MySQL")
        print("===================================")

        return True

    except mysql.connector.Error as e:

        print("Database Error :", e)

        return False

    finally:

        cursor.close()
        connection.close()


# =====================================
# Terminal Testing
# =====================================

if __name__ == "__main__":

    print("========== Student Registration ==========")

    student_name = input("Student Name : ")
    roll_number = input("Roll Number  : ")
    department = input("Department   : ")

    register_student(
        student_name,
        roll_number,
        department
    )