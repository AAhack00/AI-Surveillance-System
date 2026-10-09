import sqlite3
from datetime import datetime

def save_alert(event):

    conn = sqlite3.connect(
        "database/surveillance.db"
    )

    cursor = conn.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO alerts
        (event, timestamp)
        VALUES (?, ?)
        """,
        (event, timestamp)
    )

    conn.commit()

    conn.close()