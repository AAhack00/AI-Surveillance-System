import sqlite3

conn = sqlite3.connect("database/surveillance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    timestamp TEXT
)
""")


conn.commit()
conn.close()

print("Database Created")