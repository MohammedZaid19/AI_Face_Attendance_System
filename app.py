import streamlit as st

# ===========================================
# Page Configuration
# ===========================================

st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================
# Sidebar
# ===========================================

st.sidebar.title("🎓 AI Face Attendance")

st.sidebar.success("Navigation")

st.sidebar.info(
"""
Use the menu on the left to navigate through the application.

Modules Included

• Student Registration

• Live Attendance

• Students Database

• Attendance Reports

• Gemini AI Assistant

• Settings
"""
)

# ===========================================
# Main Page
# ===========================================

st.title("🎓 AI Face Attendance System")

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:

    st.header("Welcome")

    st.write("""
This AI Face Attendance System uses

- ✅ YuNet Face Detection

- ✅ ArcFace Face Recognition

- ✅ MySQL Database

- ✅ Google Gemini AI

- ✅ Attendance Analytics

- ✅ CSV Report Generation

to automate attendance efficiently and accurately.
""")

with col2:

    st.metric(
        label="System Status",
        value="🟢 Online"
    )

st.markdown("---")

st.subheader("Features")

c1, c2, c3 = st.columns(3)

with c1:

    st.info("""
👨‍🎓 Student Registration

Capture student images

Generate ArcFace embeddings

Store in MySQL
""")

with c2:

    st.success("""
📷 Attendance

Real-time webcam

YuNet Detection

ArcFace Recognition
""")

with c3:

    st.warning("""
🤖 Gemini AI

Attendance Chatbot

Attendance Insights

Natural Language Queries
""")

st.markdown("---")

st.header("Project Workflow")

st.code("""
Student Registration
        ↓
Capture Face
        ↓
Generate ArcFace Embedding
        ↓
Store in MySQL
        ↓
Live Webcam
        ↓
YuNet Detects Face
        ↓
ArcFace Recognizes Student
        ↓
Mark Attendance
        ↓
Generate Reports
        ↓
Gemini AI Chat
""")

st.markdown("---")

st.success("Developed using Python • Streamlit • OpenCV • YuNet • ArcFace • MySQL • Gemini AI")