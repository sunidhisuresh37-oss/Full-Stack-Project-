import sqlite3
import os

DB_FILE = "elearning.db"

def init_db():
    # Connect to the SQLite database (this creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Create Course Progress table
    # Tracking hidden stats used for AI predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_name TEXT,
            progress_percent INTEGER,
            hours_studied REAL,
            previous_score REAL,
            login_frequency REAL,
            video_completion_rate REAL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    # Check if we need to insert mock data
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        # Insert a dummy student
        cursor.execute("INSERT INTO students (name) VALUES ('Test Student')")
        student_id = cursor.lastrowid

        # Insert realistic dummy data for courses
        courses_data = [
            (student_id, 'Introduction to Deep Learning', 75, 12.5, 88.0, 0.8, 0.75),
            (student_id, 'Quantum Machine Learning', 40, 5.0, 72.5, 0.4, 0.40),
            (student_id, 'Data Science Foundations', 90, 20.0, 95.0, 0.9, 0.90),
            (student_id, 'Agile Software Engineering', 25, 3.5, 80.0, 0.3, 0.25),
            (student_id, 'Advanced Natural Language Processing', 55, 8.0, 85.0, 0.6, 0.55),
            (student_id, 'Cybersecurity & AI', 10, 1.5, 70.0, 0.2, 0.10)
        ]

        cursor.executemany("""
            INSERT INTO course_progress 
            (student_id, course_name, progress_percent, hours_studied, previous_score, login_frequency, video_completion_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, courses_data)
        
        conn.commit()

    conn.close()

def get_dashboard_data(student_id=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT course_name, progress_percent FROM course_progress WHERE student_id=?", (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"course_name": r[0], "progress_percent": r[1]} for r in rows]

def get_course_stats(student_id=1, course_name=""):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hours_studied, previous_score, login_frequency, video_completion_rate 
        FROM course_progress 
        WHERE student_id=? AND course_name=?
    """, (student_id, course_name))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "hours_studied": row[0],
            "previous_score": row[1],
            "login_frequency": row[2],
            "video_completion_rate": row[3]
        }
    return None

# Initialize the database when this file is imported
init_db()
