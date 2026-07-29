import streamlit as st
import cv2
import platform
import sys
import os
from datetime import datetime
from db import connect_database


# =====================================
# Database Status
# =====================================

def database_status():

    try:

        connection = connect_database()
        connection.close()
        return "🟢 Connected"

    except:

        return "🔴 Not Connected"


# =====================================
# Count Students
# =====================================

def total_students():

    try:

        connection = connect_database()

        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count

    except:

        return 0


# =====================================
# Count Attendance
# =====================================

def total_attendance():

    try:

        connection = connect_database()

        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM attendance")

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count

    except:

        return 0


# =====================================
# Page
# =====================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙",
    layout="wide"
)

st.title("⚙ AI Face Attendance Settings")

st.markdown("---")

# =====================================
# System Information
# =====================================

st.header("💻 System Information")

c1, c2 = st.columns(2)

with c1:

    st.info(f"Python Version : {sys.version.split()[0]}")

    st.info(f"Operating System : {platform.system()}")

    st.info(f"OpenCV Version : {cv2.__version__}")

with c2:

    st.info("Face Detector : YuNet")

    st.info("Face Recognition : ArcFace")

    st.info("Framework : DeepFace")

st.markdown("---")

# =====================================
# Database
# =====================================

st.header("🗄 Database")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Database Status",
        database_status()
    )

with c2:

    st.metric(
        "Registered Students",
        total_students()
    )

with c3:

    st.metric(
        "Attendance Records",
        total_attendance()
    )

st.markdown("---")

# =====================================
# AI Models
# =====================================

st.header("🤖 AI Models")

st.success("YuNet Face Detector")

st.success("ArcFace Face Recognition")

st.success("Gemini AI Assistant")

st.markdown("---")

# =====================================
# Project Information
# =====================================

st.header("📋 Project Information")

st.write("Project Name : AI Face Attendance System")

st.write("Version : 1.0")

st.write("Database : MySQL")

st.write("Frontend : Streamlit")

st.write("Backend : Python")

st.write("Attendance : Real-Time Face Recognition (Browser Camera)")

st.markdown("---")

# =====================================
# Maintenance
# =====================================

st.header("🧹 Maintenance")

if st.button(
    "Clear Streamlit Cache",
    use_container_width=True
):

    st.cache_data.clear()

    st.success("Cache Cleared Successfully")

if st.button(
    "Refresh Page",
    use_container_width=True
):

    st.rerun()

st.markdown("---")

# =====================================
# Footer
# =====================================

st.caption(
    f"AI Face Attendance System | {datetime.now().strftime('%d %B %Y')}"
)
