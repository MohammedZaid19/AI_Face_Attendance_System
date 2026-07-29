import mysql.connector
import csv
from datetime import datetime

from db import connect_database as _connect_database


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
# Check Duplicate Attendance
# =====================================

def attendance_exists(student_id):

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor(buffered=True)

    query = """
    SELECT COUNT(*)
    FROM attendance
    WHERE student_id = %s
    AND attendance_date = %s
    """

    today = datetime.now().date()

    cursor.execute(query, (student_id, today))

    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count > 0

# =====================================
# Mark Attendance
# =====================================

def mark_attendance(student_id, status):

    # Check duplicate attendance
    if attendance_exists(student_id):

        print("\n===================================")
        print("⚠ Attendance Already Marked Today")
        print("===================================")

        return False

    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    now = datetime.now()

    query = """
    INSERT INTO attendance
    (
        student_id,
        attendance_date,
        attendance_time,
        status
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    )
    """

    values = (
        student_id,
        now.date(),
        now.strftime("%H:%M:%S"),
        status
    )

    try:

        cursor.execute(query, values)
        connection.commit()

        print("\n===================================")
        print("✅ Attendance Marked Successfully")
        print("Student ID :", student_id)
        print("Status     :", status)
        print("Date       :", now.date())
        print("Time       :", now.strftime("%H:%M:%S"))
        print("===================================")

        return True

    except mysql.connector.Error as e:

        print("❌ Database Error :", e)
        return False

    finally:

        cursor.close()
        connection.close()


# =====================================
# Attendance Report
# =====================================

def generate_attendance_report():

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        s.student_name,
        s.roll_number,
        a.attendance_date,
        a.attendance_time,
        a.status
    FROM attendance a
    INNER JOIN students s
    ON a.student_id=s.student_id
    ORDER BY a.attendance_date DESC,
             a.attendance_time DESC
    """

    cursor.execute(query)

    records = cursor.fetchall()

    print("\n==============================================")
    print("Attendance Report")
    print("==============================================")

    for record in records:

        print(
            f"{record['student_name']} | "
            f"{record['roll_number']} | "
            f"{record['attendance_date']} | "
            f"{record['attendance_time']} | "
            f"{record['status']}"
        )

    print("\nTotal Records :", len(records))

    cursor.close()
    connection.close()


# =====================================
# Export Attendance To CSV
# =====================================

def export_attendance_csv(filename="attendance_report.csv"):

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    query = """
    SELECT
        student_id,
        attendance_date,
        attendance_time,
        status
    FROM attendance
    """

    cursor.execute(query)

    records = cursor.fetchall()

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Date",
            "Time",
            "Status"
        ])

        writer.writerows(records)

    cursor.close()
    connection.close()

    print("\n✅ CSV Exported Successfully")
    print("File :", filename)


# =====================================
# Attendance Summary
# =====================================

def attendance_summary():

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    today = datetime.now().date()

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE attendance_date=%s AND status='Present'",
        (today,)
    )

    present = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE attendance_date=%s AND status='Absent'",
        (today,)
    )

    absent = cursor.fetchone()[0]

    print("\n===================================")
    print("Today's Attendance Summary")
    print("===================================")
    print("Present :", present)
    print("Absent  :", absent)

    cursor.close()
    connection.close()


# =====================================
# Testing
# =====================================

if __name__ == "__main__":
    generate_attendance_report()
    attendance_summary()
    export_attendance_csv()
