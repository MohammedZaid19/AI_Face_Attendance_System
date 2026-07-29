import os
import json
import cv2
import mysql.connector

from db import connect_database as _connect_database
from models.yunet_detector import detect_faces
from models.sface_recognizer import get_embedding


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
# Generate SFace Embedding
#
# Detects the face in the captured photo
# using YuNet, then generates a 128-d
# SFace embedding for it. Returns None
# if no face was detected.
# =====================================

def generate_embedding(face_image_bgr):

    faces = detect_faces(face_image_bgr)

    if faces is None or len(faces) == 0:
        return None

    # Use the first detected face
    face_row = faces[0]

    embedding = get_embedding(face_image_bgr, face_row)

    return embedding.flatten().tolist()


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
    # Generate SFace Embedding
    # ----------------------------

    try:

        embedding = generate_embedding(face_image_bgr)

        if embedding is None:

            print("❌ No Face Detected In Captured Photo")

            cursor.close()
            connection.close()

            return False

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
        print("✅ SFace Embedding Generated")
        print("✅ Embedding Stored in MySQL")
        print("===================================")

        return True

    except mysql.connector.Error as e:

        print("Database Error :", e)

        return False

    finally:

        cursor.close()
        connection.close()
