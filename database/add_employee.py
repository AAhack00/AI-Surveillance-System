import sqlite3

conn = sqlite3.connect(
    "database/surveillance.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO users
    VALUES
    (
        NULL,
        'arnav',
        'arnav123',
        'employee'
    )
    """
)

conn.commit()

conn.close()

print("Employee Added")