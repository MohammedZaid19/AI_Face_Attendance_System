import streamlit as st
import mysql.connector
from attendance import start_attendance


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
# Attendance Button
# =====================================

st.subheader("Live Face Attendance")

st.info(
"""
Click the button below to start the webcam.

The system will

• Detect Face using YuNet

• Generate ArcFace Embedding

• Match with Database

• Mark Attendance Automatically
"""
)

if st.button(
    "▶ Start Attendance",
    use_container_width=True
):

    with st.spinner("Opening Webcam..."):

        start_attendance()

    st.success("Attendance Session Finished")


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