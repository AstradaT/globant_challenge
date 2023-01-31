import sqlite3


def get_data(table: str):
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    result = cur.execute(f"SELECT * FROM {table};").fetchall()
    return result