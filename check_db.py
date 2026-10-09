import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "database/surveillance.db"
)

df = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)

print(df)

print("\nColumns:")

print(df.columns)