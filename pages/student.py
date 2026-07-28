# import streamlit as st
# import mysql.connector
# import pandas as pd
# import os
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
# # Load Students
# # =====================================
#
# def load_students():
#
#     connection = connect_database()
#
#     cursor = connection.cursor(dictionary=True)
#
#     cursor.execute("""
#         SELECT
#             student_id,
#             student_name,
#             roll_number,
#             department,
#             image_path
#         FROM students
#         ORDER BY student_name
#     """)
#
#     students = cursor.fetchall()
#
#     cursor.close()
#     connection.close()
#
#     return students
#
#
# # =====================================
# # Delete Student
# # =====================================
#
# def delete_student(student_id):
#
#     connection = connect_database()
#
#     cursor = connection.cursor()
#
#     try:
#
#         cursor.execute(
#             "DELETE FROM students WHERE student_id=%s",
#             (student_id,)
#         )
#
#         connection.commit()
#
#     finally:
#
#         cursor.close()
#         connection.close()
#
#
# # =====================================
# # Page
# # =====================================
#
# st.set_page_config(
#     page_title="Students",
#     page_icon="👨‍🎓",
#     layout="wide"
# )
#
# st.title("👨‍🎓 Registered Students")
#
# st.markdown("---")
#
# students = load_students()
#
# st.metric(
#     "Total Registered Students",
#     len(students)
# )
#
# st.markdown("---")
#
# # =====================================
# # Search
# # =====================================
#
# search = st.text_input(
#     "🔍 Search Student",
#     placeholder="Enter Name or Roll Number"
# )
#
# if search:
#
#     students = [
#
#         s for s in students
#
#         if search.lower() in s["student_name"].lower()
#
#         or search.lower() in s["roll_number"].lower()
#
#     ]
#
# # =====================================
# # Student List
# # =====================================
#
# if len(students) == 0:
#
#     st.warning("No Students Found")
#
# else:
#
#     for student in students:
#
#         with st.container():
#
#             col1, col2, col3 = st.columns([1,4,1])
#
#             # Image
#             with col1:
#
#                 if os.path.exists(student["image_path"]):
#
#                     st.image(
#                         student["image_path"],
#                         width=120
#                     )
#
#                 else:
#
#                     st.image(
#                         "https://via.placeholder.com/120",
#                         width=120
#                     )
#
#             # Details
#             with col2:
#
#                 st.subheader(student["student_name"])
#
#                 st.write(
#                     f"**Roll Number:** {student['roll_number']}"
#                 )
#
#                 st.write(
#                     f"**Department:** {student['department']}"
#                 )
#
#                 st.write(
#                     f"**Student ID:** {student['student_id']}"
#                 )
#
#             # Delete
#             with col3:
#
#                 if st.button(
#                     "🗑 Delete",
#                     key=student["student_id"]
#                 ):
#
#                     delete_student(student["student_id"])
#
#                     st.success("Student Deleted Successfully")
#
#                     st.rerun()
#
#             st.divider()
#
# # =====================================
# # Data Table
# # =====================================
#
# st.subheader("Student Database")
#
# table = pd.DataFrame(students)
#
# if not table.empty:
#
#     st.dataframe(
#         table,
#         use_container_width=True,
#         hide_index=True
#     )
#
# # =====================================
# # Refresh
# # =====================================
#
# if st.button("🔄 Refresh"):
#
#     st.rerun()
#
# st.markdown("---")
#
# st.caption("AI Face Attendance System • Students Module")
import streamlit as st
import pandas as pd
import os
from db import connect_database


# =====================================
# Load Students
# =====================================

def load_students():

    connection = connect_database()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            student_id,
            student_name,
            roll_number,
            department,
            image_path
        FROM students
        ORDER BY student_name
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students


# =====================================
# Delete Student
# =====================================

def delete_student(student_id):

    connection = connect_database()

    cursor = connection.cursor()

    try:

        cursor.execute(
            "DELETE FROM students WHERE student_id=%s",
            (student_id,)
        )

        connection.commit()

    finally:

        cursor.close()
        connection.close()


# =====================================
# Page
# =====================================

st.set_page_config(
    page_title="Students",
    page_icon="👨‍🎓",
    layout="wide"
)

st.title("👨‍🎓 Registered Students")

st.markdown("---")

students = load_students()

st.metric(
    "Total Registered Students",
    len(students)
)

st.markdown("---")

# =====================================
# Search
# =====================================

search = st.text_input(
    "🔍 Search Student",
    placeholder="Enter Name or Roll Number"
)

if search:

    students = [

        s for s in students

        if search.lower() in s["student_name"].lower()

        or search.lower() in s["roll_number"].lower()

    ]

# =====================================
# Student List
# =====================================

if len(students) == 0:

    st.warning("No Students Found")

else:

    for student in students:

        with st.container():

            col1, col2, col3 = st.columns([1,4,1])

            # Image
            with col1:

                if os.path.exists(student["image_path"]):

                    st.image(
                        student["image_path"],
                        width=120
                    )

                else:

                    st.image(
                        "https://via.placeholder.com/120",
                        width=120
                    )

            # Details
            with col2:

                st.subheader(student["student_name"])

                st.write(
                    f"**Roll Number:** {student['roll_number']}"
                )

                st.write(
                    f"**Department:** {student['department']}"
                )

                st.write(
                    f"**Student ID:** {student['student_id']}"
                )

            # Delete
            with col3:

                if st.button(
                    "🗑 Delete",
                    key=student["student_id"]
                ):

                    delete_student(student["student_id"])

                    st.success("Student Deleted Successfully")

                    st.rerun()

            st.divider()

# =====================================
# Data Table
# =====================================

st.subheader("Student Database")

table = pd.DataFrame(students)

if not table.empty:

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

# =====================================
# Refresh
# =====================================

if st.button("🔄 Refresh"):

    st.rerun()

st.markdown("---")

st.caption("AI Face Attendance System • Students Module")