import streamlit as st
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
    "📷 Capture Face & Register Student",
    use_container_width=True
):

    if (
        student_name.strip() == "" or
        roll_number.strip() == "" or
        department.strip() == ""
    ):

        st.warning("Please fill all the fields.")

    else:

        with st.spinner("Opening webcam..."):

            success = register_student(
                student_name,
                roll_number,
                department
            )

        if success:

            st.success("🎉 Student Registered Successfully!")

            st.balloons()

        else:

            st.error("Registration Failed!")

# =====================================
# Workflow
# =====================================

st.markdown("---")

st.subheader("📌 Registration Workflow")

st.code(
"""
Student Details
       ↓
Capture Face (Webcam)
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

• Captures the student's face using the webcam

• Detects the face using YuNet

• Generates a 512-dimensional ArcFace embedding

• Saves the captured image

• Stores student details in the MySQL database

• Stores the face embedding in the face_embeddings table
"""
)