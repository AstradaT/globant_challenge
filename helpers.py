import sqlite3


def get_data(table: str):
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    result = cur.execute(f"SELECT * FROM {table};").fetchall()
    return result


schema_d = {
    'name': 'Departments',
    'namespace': 'globant',
    'type': 'record',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'department', 'type': 'string'},
    ],
    }

schema_e = {
    'name': 'Employees',
    'namespace': 'globant',
    'type': 'record',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'name', 'type': 'string'},
        {'name': 'datetime', 'type': 'string'},
        {'name': 'department_id', 'type': 'int'},
        {'name': 'job_id', 'type': 'int'},
    ],
    }

schema_j = {
    'name': 'Jobs',
    'namespace': 'globant',
    'type': 'record',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'job', 'type': 'string'},
    ],
    }