import streamlit as st
import numpy as np
import cv2
from PIL import Image
from main import register_student

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Student Registration",
    page_icon="🎓",
    layout="wide"
)

# =====================================
# Header
# =====================================

st.title("🎓 Student Registration")

st.markdown(
    "Register a new student by entering the details below."
)

st.markdown("---")

# =====================================
# Layout
# =====================================

left, right = st.columns([2, 1])

# =====================================
# Left Column
# =====================================

with left:

    st.subheader("Student Details")

    student_name = st.text_input(
        "👤 Student Name"
    )

    roll_number = st.text_input(
        "🆔 Roll Number"
    )

    department = st.text_input(
        "🏫 Department"
    )

    st.subheader("📷 Capture Face")

    photo = st.camera_input(
        "Look at the camera and take a photo"
    )

# =====================================
# Right Column
# =====================================

with right:

    st.subheader("Registration Process")

    st.success("📷 Capture Face")

    st.success("🧠 Generate ArcFace Embedding")

    st.success("💾 Save to MySQL")

    st.success("✅ Registration Complete")

# =====================================
# Register Button
# =====================================

st.markdown("---")

if st.button(
    "📷 Register Student",
    use_container_width=True
):

    if (
        student_name.strip() == "" or
        roll_number.strip() == "" or
        department.strip() == ""
    ):

        st.warning("Please fill all the fields.")

    elif photo is None:

        st.warning("Please capture a photo using the camera above.")

    else:

        with st.spinner("Processing face and saving student..."):

            # Convert the captured photo (browser camera) into
            # a BGR numpy array, the format OpenCV/DeepFace expect
            image = Image.open(photo)

            face_image_bgr = cv2.cvtColor(
                np.array(image.convert("RGB")),
                cv2.COLOR_RGB2BGR
            )

            success = register_student(
                student_name,
                roll_number,
                department,
                face_image_bgr
            )

        if success:

            st.success("🎉 Student Registered Successfully!")

            st.balloons()

        else:

            st.error("Registration Failed! Please check the photo and try again.")

# =====================================
# Workflow
# =====================================

st.markdown("---")

st.subheader("📌 Registration Workflow")

st.code(
"""
Student Details
       ↓
Capture Face (Browser Camera)
       ↓
YuNet Detects Face
       ↓
Generate ArcFace Embedding
       ↓
Store Student Details
       ↓
Store Face Embedding
       ↓
Registration Completed
"""
)

# =====================================
# Information
# =====================================

st.markdown("---")

st.info(
"""
The registration process performs the following operations automatically:

• Captures the student's face using your browser's camera

• Detects the face using YuNet

• Generates a 512-dimensional ArcFace embedding

• Saves the captured image

• Stores student details in the MySQL database

• Stores the face embedding in the face_embeddings table
"""
)
