import sqlite3
from fastavro import reader
import json


def get_data(table:str, offset:int, limit:int):
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    result = cur.execute(f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset};").fetchall()
    return result


def read_avro(table: str):
    with open(f'data/{table}.avro', 'rb') as file:
        avro_reader = reader(file)
        records = [r for r in avro_reader]

    return json.dumps(records)


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
        {'name': 'name', 'type': ['string', 'null']},
        {'name': 'datetime', 'type': ['string', 'null']},
        {'name': 'department_id', 'type': ['int', 'null']},
        {'name': 'job_id', 'type': ['int', 'null']},
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