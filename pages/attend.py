import streamlit as st
import numpy as np
import cv2
from PIL import Image

from attendance import process_attendance_frame
from db import connect_database


# =====================================
# Dashboard Statistics
# =====================================

def get_statistics():

    connection = connect_database()

    cursor = connection.cursor()

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Present Today
    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = CURDATE()
        AND status='Present'
    """)
    present = cursor.fetchone()[0]

    # Absent Today
    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = CURDATE()
        AND status='Absent'
    """)
    absent = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_students, present, absent


# =====================================
# Attendance Records
# =====================================

def load_attendance():

    connection = connect_database()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        s.student_name,
        s.roll_number,
        a.attendance_date,
        a.attendance_time,
        a.status
    FROM attendance a
    JOIN students s
    ON a.student_id=s.student_id
    ORDER BY a.attendance_date DESC,
             a.attendance_time DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records


# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Attendance",
    page_icon="📸",
    layout="wide"
)

st.title("📸 AI Face Attendance")

st.markdown("---")


# =====================================
# Statistics
# =====================================

total, present, absent = get_statistics()

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "👨‍🎓 Registered Students",
        total
    )

with c2:

    st.metric(
        "✅ Present Today",
        present
    )

with c3:

    st.metric(
        "❌ Absent Today",
        absent
    )


st.markdown("---")


# =====================================
# Attendance Capture
# =====================================

st.subheader("Live Face Attendance")

st.info(
"""
Click below to open your camera and take a photo.

The system will

• Detect Face using YuNet

• Generate ArcFace Embedding

• Match with Database

• Mark Attendance Automatically
"""
)

photo = st.camera_input(
    "📷 Capture Attendance Photo"
)

if photo is not None:

    with st.spinner("Analyzing photo..."):

        image = Image.open(photo)

        frame = cv2.cvtColor(
            np.array(image.convert("RGB")),
            cv2.COLOR_RGB2BGR
        )

        annotated_frame, results = process_attendance_frame(frame)

        annotated_rgb = cv2.cvtColor(
            annotated_frame,
            cv2.COLOR_BGR2RGB
        )

    st.image(
        annotated_rgb,
        caption="Detected Faces",
        use_container_width=True
    )

    if len(results) == 0:

        st.error("No registered face recognized in this photo. Please try again.")

    else:

        for result in results:

            if result["marked"]:

                st.success(
                    f"✅ {result['name']} ({result['roll_number']}) "
                    f"marked present — match confidence {result['score']:.2f}"
                )

            else:

                st.warning(
                    f"⚠ {result['name']} ({result['roll_number']}) "
                    f"was already marked present today."
                )


st.markdown("---")


# =====================================
# Attendance Records
# =====================================

st.subheader("Today's Attendance Records")

records = load_attendance()

if len(records) == 0:

    st.warning("No Attendance Records Found")

else:

    st.dataframe(
        records,
        use_container_width=True,
        hide_index=True
    )


st.markdown("---")

st.caption("AI Face Attendance System using YuNet + ArcFace + DeepFace")
