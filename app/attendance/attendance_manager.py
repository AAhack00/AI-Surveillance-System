import sqlite3
from datetime import datetime


def process_attendance(name):

    conn = sqlite3.connect(
        "database/surveillance.db"
    )

    cursor = conn.cursor()

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    current_dt = datetime.now()

    cursor.execute(
        """
        SELECT check_in, check_out
        FROM attendance
        WHERE name=? AND date=?
        """,
        (name, today)
    )

    record = cursor.fetchone()

    # -----------------
    # FIRST ENTRY
    # -----------------

    if record is None:

        cursor.execute(
            """
            INSERT INTO attendance
            (
                name,
                date,
                check_in,
                check_out
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                today,
                current_time,
                ""
            )
        )

        conn.commit()

        conn.close()

        return "IN"

    check_in = record[0]
    check_out = record[1]

    # -----------------
    # ALREADY CHECKED OUT
    # -----------------

    if check_out != "":

        conn.close()

        return "DONE"

    # -----------------
    # CHECK TIME DIFFERENCE
    # -----------------

    checkin_dt = datetime.strptime(
        today + " " + check_in,
        "%Y-%m-%d %H:%M:%S"
    )

    difference = (
        current_dt - checkin_dt
    ).total_seconds()

    if difference >= 300:

        cursor.execute(
            """
            UPDATE attendance
            SET check_out=?
            WHERE name=? AND date=?
            """,
            (
                current_time,
                name,
                today
            )
        )

        conn.commit()

        conn.close()

        return "OUT"

    conn.close()

    return "WAIT"