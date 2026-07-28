# # # from google import genai
# # # import mysql.connector
# # #
# # # # =====================================
# # # # Gemini API Key
# # # # =====================================
# # #
# # # API_KEY = ""
# # #
# # # client = genai.Client(api_key=API_KEY)
# # #
# # #
# # # # =====================================
# # # # Database Connection
# # # # =====================================
# # #
# # # def connect_database():
# # #
# # #     return mysql.connector.connect(
# # #         host="localhost",
# # #         user="root",
# # #         password="zaid08",
# # #         database="ai_face_attendance"
# # #     )
# # #
# # #
# # # # =====================================
# # # # Load Attendance Data
# # # # =====================================
# # #
# # # def load_attendance():
# # #
# # #     connection = connect_database()
# # #
# # #     cursor = connection.cursor(dictionary=True)
# # #
# # #     query = """
# # #     SELECT
# # #         s.student_name,
# # #         s.roll_number,
# # #         a.attendance_date,
# # #         a.attendance_time,
# # #         a.status
# # #     FROM attendance a
# # #     INNER JOIN students s
# # #     ON a.student_id = s.student_id
# # #     """
# # #
# # #     cursor.execute(query)
# # #
# # #     records = cursor.fetchall()
# # #
# # #     cursor.close()
# # #     connection.close()
# # #
# # #     return records
# # #
# # #
# # # # =====================================
# # # # Ask Gemini
# # # # =====================================
# # #
# # # def ask_gemini(question):
# # #
# # #     records = load_attendance()
# # #
# # #     attendance_text = ""
# # #
# # #     for record in records:
# # #
# # #         attendance_text += (
# # #             f"Name: {record['student_name']}, "
# # #             f"Roll: {record['roll_number']}, "
# # #             f"Date: {record['attendance_date']}, "
# # #             f"Time: {record['attendance_time']}, "
# # #             f"Status: {record['status']}\n"
# # #         )
# # #
# # #     prompt = f"""
# # # You are an AI Attendance Assistant.
# # #
# # # Attendance Records:
# # #
# # # {attendance_text}
# # #
# # # Answer this question:
# # #
# # # {question}
# # # """
# # #
# # #     response = client.models.generate_content(
# # #         model="gemini-3.5-flash",
# # #         contents=prompt
# # #     )
# # #
# # #     print("\nGemini Response\n")
# # #     print(response.text)
# # #
# # #
# # # # =====================================
# # # # Testing
# # # # =====================================
# # #
# # # if __name__ == "__main__":
# # #
# # #     while True:
# # #
# # #         question = input("\nAsk Gemini (type 'exit' to quit): ")
# # #
# # #         if question.lower() == "exit":
# # #             break
# # #
# # #         ask_gemini(question)
# # import os
# # from dotenv import load_dotenv
# # from google import genai
# # import mysql.connector
# #
# # # Load environment variables from the .env file
# # load_dotenv()
# #
# # # =====================================
# # # Gemini API Key (Loaded Securely from .env)
# # # =====================================
# #
# # API_KEY = os.getenv("GEMINI_API_KEY")
# #
# # client = genai.Client(api_key=API_KEY)
# #
# #
# # # =====================================
# # # Database Connection (Loaded Securely from .env)
# # # =====================================
# #
# # def connect_database():
# #
# #     return mysql.connector.connect(
# #         host=os.getenv("DB_HOST", "localhost"),
# #         user=os.getenv("DB_USER", "root"),
# #         password=os.getenv("DB_PASSWORD"),
# #         database=os.getenv("DB_NAME", "ai_face_attendance")
# #     )
# #
# #
# # # =====================================
# # # Load Attendance Data
# # # =====================================
# #
# # def load_attendance():
# #
# #     connection = connect_database()
# #
# #     cursor = connection.cursor(dictionary=True)
# #
# #     query = """
# #     SELECT
# #         s.student_name,
# #         s.roll_number,
# #         a.attendance_date,
# #         a.attendance_time,
# #         a.status
# #     FROM attendance a
# #     INNER JOIN students s
# #     ON a.student_id = s.student_id
# #     """
# #
# #     cursor.execute(query)
# #
# #     records = cursor.fetchall()
# #
# #     cursor.close()
# #     connection.close()
# #
# #     return records
# #
# #
# # # =====================================
# # # Ask Gemini
# # # =====================================
# #
# # def ask_gemini(question):
# #
# #     records = load_attendance()
# #
# #     attendance_text = ""
# #
# #     for record in records:
# #
# #         attendance_text += (
# #             f"Name: {record['student_name']}, "
# #             f"Roll: {record['roll_number']}, "
# #             f"Date: {record['attendance_date']}, "
# #             f"Time: {record['attendance_time']}, "
# #             f"Status: {record['status']}\n"
# #         )
# #
# #     prompt = f"""
# # You are an AI Attendance Assistant.
# #
# # Attendance Records:
# #
# # {attendance_text}
# #
# # Answer this question:
# #
# # {question}
# # """
# #
# #     response = client.models.generate_content(
# #         model="gemini-3.5-flash",
# #         contents=prompt
# #     )
# #
# #     print("\nGemini Response\n")
# #     print(response.text)
# #
# #
# # # =====================================
# # # Testing
# # # =====================================
# #
# # if __name__ == "__main__":
# #
# #     while True:
# #
# #         question = input("\nAsk Gemini (type 'exit' to quit): ")
# #
# #         if question.lower() == "exit":
# #             break
# #
# #         ask_gemini(question)
# import os
# import mysql.connector
# from dotenv import load_dotenv
# from google import genai
#
# # =====================================
# # Load Environment Variables
# # =====================================
#
# load_dotenv()
#
# API_KEY = os.getenv("GEMINI_API_KEY")
#
# client = genai.Client(api_key=API_KEY)
#
#
# # =====================================
# # Database Connection
# # =====================================
#
# def connect_database():
#
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST", "localhost"),
#         user=os.getenv("DB_USER", "root"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME", "ai_face_attendance")
#     )
#
#
# # =====================================
# # Load Attendance Records
# # =====================================
#
# def load_attendance():
#
#     connection = connect_database()
#
#     cursor = connection.cursor(dictionary=True)
#
#     cursor.execute("""
#     SELECT
#         s.student_name,
#         s.roll_number,
#         a.attendance_date,
#         a.attendance_time,
#         a.status
#     FROM attendance a
#     INNER JOIN students s
#     ON a.student_id = s.student_id
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
# # Build Prompt
# # =====================================
#
# def build_prompt(question):
#
#     records = load_attendance()
#
#     attendance_text = ""
#
#     for record in records:
#
#         attendance_text += (
#             f"Student : {record['student_name']}\n"
#             f"Roll No : {record['roll_number']}\n"
#             f"Date : {record['attendance_date']}\n"
#             f"Time : {record['attendance_time']}\n"
#             f"Status : {record['status']}\n\n"
#         )
#
#     prompt = f"""
# You are an AI Face Attendance Assistant.
#
# You answer ONLY questions related to attendance.
#
# Attendance Records
#
# {attendance_text}
#
# Answer the following question clearly.
#
# Question:
# {question}
# """
#
#     return prompt
#
#
# # =====================================
# # Ask Gemini (Returns Text)
# # =====================================
#
# def ask_gemini_streamlit(question):
#
#     try:
#
#         prompt = build_prompt(question)
#
#         response = client.models.generate_content(
#             model="gemini-3.5-flash",
#             contents=prompt
#         )
#
#         return response.text
#
#     except Exception as e:
#
#         return f"❌ Gemini Error\n\n{e}"
#
#
# # =====================================
# # Terminal Chatbot
# # =====================================
#
# def ask_gemini(question):
#
#     answer = ask_gemini_streamlit(question)
#
#     print("\n====================================")
#     print("Gemini Response")
#     print("====================================\n")
#
#     print(answer)
#
#
# # =====================================
# # Main
# # =====================================
#
# if __name__ == "__main__":
#
#     print("=" * 50)
#     print(" AI Face Attendance Gemini Chat")
#     print("=" * 50)
#
#     while True:
#
#         question = input("\nAsk Gemini (type 'exit' to quit): ")
#
#         if question.lower() == "exit":
#             break
#
#         ask_gemini(question)
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from db import connect_database

# =====================================
# Load Environment Variables (for local
# development only - Streamlit Cloud
# uses st.secrets instead)
# =====================================

load_dotenv()

API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=API_KEY)


# =====================================
# Load Attendance Records
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
    INNER JOIN students s
    ON a.student_id = s.student_id
    ORDER BY
        a.attendance_date DESC,
        a.attendance_time DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records


# =====================================
# Build Prompt
# =====================================

def build_prompt(question):

    records = load_attendance()

    attendance_text = ""

    for record in records:

        attendance_text += (
            f"Student : {record['student_name']}\n"
            f"Roll No : {record['roll_number']}\n"
            f"Date : {record['attendance_date']}\n"
            f"Time : {record['attendance_time']}\n"
            f"Status : {record['status']}\n\n"
        )

    prompt = f"""
You are an AI Face Attendance Assistant.

You answer ONLY questions related to attendance.

Attendance Records

{attendance_text}

Answer the following question clearly.

Question:
{question}
"""

    return prompt


# =====================================
# Ask Gemini (Returns Text)
# =====================================

def ask_gemini_streamlit(question):

    try:

        prompt = build_prompt(question)

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Gemini Error\n\n{e}"


# =====================================
# Terminal Chatbot
# =====================================

def ask_gemini(question):

    answer = ask_gemini_streamlit(question)

    print("\n====================================")
    print("Gemini Response")
    print("====================================\n")

    print(answer)


# =====================================
# Main
# =====================================

if __name__ == "__main__":

    print("=" * 50)
    print(" AI Face Attendance Gemini Chat")
    print("=" * 50)

    while True:

        question = input("\nAsk Gemini (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        ask_gemini(question)