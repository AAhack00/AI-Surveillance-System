import sqlite3
from datetime import datetime

conn = sqlite3.connect(
    "database/surveillance.db"
)

cursor = conn.cursor()


# -----------------------------
# Reset Auto Increment
# -----------------------------
def reset_sequence(table):

    cursor.execute(
        f"SELECT MAX(id) FROM {table}"
    )

    result = cursor.fetchone()

    max_id = result[0]

    if max_id is None:
        max_id = 0

    cursor.execute(
        """
        UPDATE sqlite_sequence
        SET seq=?
        WHERE name=?
        """,
        (
            max_id,
            table
        )
    )


print("\n===== DATABASE MANAGER =====\n")

print("1. Attendance")
print("2. Alerts")

table_choice = input(
    "\nChoose table (1/2): "
)

if table_choice == "1":

    table = "attendance"

elif table_choice == "2":

    table = "alerts"

else:

    print("Invalid Choice")

    conn.close()

    exit()

print("\n1. Delete Today's Records")
print("2. Delete Specific Date")
print("3. Delete All Records")
print("4. Delete By Name")

choice = input(
    "\nChoose option: "
)

# ---------------------------------------
# DELETE TODAY
# ---------------------------------------

if choice == "1":

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    if table == "attendance":

        cursor.execute(
            "DELETE FROM attendance WHERE date=?",
            (today,)
        )

    else:

        cursor.execute(
            "DELETE FROM alerts WHERE timestamp LIKE ?",
            (today + "%",)
        )

    reset_sequence(table)

    print(
        "\nToday's Records Deleted."
    )

# ---------------------------------------
# DELETE SPECIFIC DATE
# ---------------------------------------

elif choice == "2":

    date = input(
        "\nEnter Date (YYYY-MM-DD): "
    )

    if table == "attendance":

        cursor.execute(
            "DELETE FROM attendance WHERE date=?",
            (date,)
        )

    else:

        cursor.execute(
            "DELETE FROM alerts WHERE timestamp LIKE ?",
            (date + "%",)
        )

    reset_sequence(table)

    print(
        "\nRecords Deleted."
    )

# ---------------------------------------
# DELETE ALL
# ---------------------------------------

elif choice == "3":

    confirm = input(
        "\nDelete ALL Records? (yes/no): "
    )

    if confirm.lower() == "yes":

        cursor.execute(
            f"DELETE FROM {table}"
        )

        cursor.execute(
            """
            UPDATE sqlite_sequence
            SET seq=0
            WHERE name=?
            """,
            (table,)
        )

        print(
            "\nAll Records Deleted."
        )

    else:

        print(
            "\nCancelled."
        )

# ---------------------------------------
# DELETE BY NAME
# ---------------------------------------

elif choice == "4":

    if table != "attendance":

        print(
            "\nDelete By Name only available for Attendance."
        )

    else:

        name = input(
            "\nEnter Employee Name: "
        )

        cursor.execute(
            """
            DELETE FROM attendance
            WHERE name=?
            """,
            (name,)
        )

        reset_sequence(table)

        print(
            "\nAttendance Deleted."
        )

else:

    print(
        "\nInvalid Option."
    )

conn.commit()

conn.close()

print("\nDatabase Updated Successfully.")