import sqlite3

conn = sqlite3.connect(
    "database/surveillance.db"
)

cursor = conn.cursor()

cursor.execute(
    "DROP TABLE IF EXISTS attendance"
)

cursor.execute("""
CREATE TABLE attendance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    date TEXT,

    check_in TEXT,

    check_out TEXT
)
""")

conn.commit()

conn.close()

print("Attendance table created.")