import os
import json
import cv2
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
# Save Captured Face Image
#
# face_image_bgr is a numpy array (BGR
# format) coming from the browser camera
# (st.camera_input), already captured -
# no webcam access happens here.
# =====================================

def save_face_image(face_image_bgr, roll_number):

    if not os.path.exists("images"):
        os.makedirs("images")

    image_path = f"images/{roll_number}.jpg"

    cv2.imwrite(image_path, face_image_bgr)

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
#
# face_image_bgr: numpy array (BGR) of
# the already-captured photo from the
# browser camera widget.
# =====================================

def register_student(student_name,
                     roll_number,
                     department,
                     face_image_bgr):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    # ----------------------------
    # Save Captured Face Image
    # ----------------------------

    image_path = save_face_image(face_image_bgr, roll_number)

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
