import sqlite3

name = input(
    "Employee Name: "
)

conn = sqlite3.connect(
    "database/surveillance.db"
)

cursor = conn.cursor()

cursor.execute(
    "DELETE FROM users WHERE username=?",
    (name,)
)

conn.commit()

conn.close()

print(
    "Employee Deleted."
)