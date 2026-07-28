# import streamlit as st
# import mysql.connector
# import pandas as pd
# from attendance_utils import export_attendance_csv
#
# # =====================================
# # Database Connection
# # =====================================
#
# def connect_database():
#
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="zaid08",
#         database="ai_face_attendance"
#     )
#
#
# # =====================================
# # Load Attendance Report
# # =====================================
#
# def load_report():
#
#     connection = connect_database()
#
#     cursor = connection.cursor(dictionary=True)
#
#     cursor.execute("""
#     SELECT
#         s.student_name,
#         s.roll_number,
#         s.department,
#         a.attendance_date,
#         a.attendance_time,
#         a.status
#     FROM attendance a
#     JOIN students s
#     ON a.student_id=s.student_id
#     ORDER BY
#         a.attendance_date DESC,
#         a.attendance_time DESC
#     """)
#
#     records = cursor.fetchall()
#
#     cursor.close()
#     connection.close()
#
#     return records
#
#
# # =====================================
# # Page
# # =====================================
#
# st.set_page_config(
#     page_title="Attendance Reports",
#     page_icon="📄",
#     layout="wide"
# )
#
# st.title("📄 Attendance Reports")
#
# st.markdown("---")
#
# records = load_report()
#
# # =====================================
# # Statistics
# # =====================================
#
# total = len(records)
#
# present = len(
#     [r for r in records if r["status"] == "Present"]
# )
#
# absent = len(
#     [r for r in records if r["status"] == "Absent"]
# )
#
# c1, c2, c3 = st.columns(3)
#
# with c1:
#     st.metric("Total Records", total)
#
# with c2:
#     st.metric("Present", present)
#
# with c3:
#     st.metric("Absent", absent)
#
# st.markdown("---")
#
# # =====================================
# # Search
# # =====================================
#
# search = st.text_input(
#     "🔍 Search Student"
# )
#
# if search:
#
#     records = [
#
#         r for r in records
#
#         if search.lower() in r["student_name"].lower()
#
#         or search.lower() in r["roll_number"].lower()
#
#     ]
#
# # =====================================
# # Attendance Table
# # =====================================
#
# st.subheader("Attendance Report")
#
# df = pd.DataFrame(records)
#
# st.dataframe(
#     df,
#     use_container_width=True,
#     hide_index=True
# )
#
# st.markdown("---")
#
# # =====================================
# # Export Report
# # =====================================
#
# st.subheader("Export Attendance")
#
# if st.button(
#     "📥 Generate CSV Report",
#     use_container_width=True
# ):
#
#     export_attendance_csv()
#
#     st.success("CSV Report Generated Successfully!")
#
# st.markdown("---")
#
# st.caption("AI Face Attendance System • Reports")
import streamlit as st
import pandas as pd
from attendance_utils import export_attendance_csv
from db import connect_database


# =====================================
# Load Attendance Report
# =====================================

def load_report():

    connection = connect_database()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        s.student_name,
        s.roll_number,
        s.department,
        a.attendance_date,
        a.attendance_time,
        a.status
    FROM attendance a
    JOIN students s
    ON a.student_id=s.student_id
    ORDER BY
        a.attendance_date DESC,
        a.attendance_time DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records


# =====================================
# Page
# =====================================

st.set_page_config(
    page_title="Attendance Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Attendance Reports")

st.markdown("---")

records = load_report()

# =====================================
# Statistics
# =====================================

total = len(records)

present = len(
    [r for r in records if r["status"] == "Present"]
)

absent = len(
    [r for r in records if r["status"] == "Absent"]
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Records", total)

with c2:
    st.metric("Present", present)

with c3:
    st.metric("Absent", absent)

st.markdown("---")

# =====================================
# Search
# =====================================

search = st.text_input(
    "🔍 Search Student"
)

if search:

    records = [

        r for r in records

        if search.lower() in r["student_name"].lower()

        or search.lower() in r["roll_number"].lower()

    ]

# =====================================
# Attendance Table
# =====================================

st.subheader("Attendance Report")

df = pd.DataFrame(records)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================
# Export Report
# =====================================

st.subheader("Export Attendance")

if st.button(
    "📥 Generate CSV Report",
    use_container_width=True
):

    export_attendance_csv()

    st.success("CSV Report Generated Successfully!")

st.markdown("---")

st.caption("AI Face Attendance System • Reports")