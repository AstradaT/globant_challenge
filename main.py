import json
import os
import pandas as pd
import sqlite3
from fastavro import writer
from flask import Flask, jsonify, request, render_template, flash, send_file, redirect
from flask_sqlalchemy import SQLAlchemy
from helpers import get_data, schema_d, schema_e, schema_j, read_avro
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'data'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    department = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Department(id={self.id}, department={self.department})>"

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String)
    datetime = db.Column(db.String)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    department = db.relationship('Department')
    job = db.relationship('Job')

    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name})>"

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    job = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Job(id={self.id}, job={self.job})>"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get file from html form
        file = request.files['file']
        if file.filename != '':
            # Save file to storage
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            # Convert csv to dataframe
            df = pd.read_csv(filepath, header=None)
            # Move data to SQLite database
            with db.engine.begin() as conn:
                table = file.filename
                df.to_sql(table, con=conn, if_exists='replace', index=False, chunksize=1000)
                table_2 = table.removeprefix('hired_').removesuffix('.csv')
                try:
                    conn.execute(f"INSERT INTO {table_2} SELECT * FROM `{table}`;")
                    message = "The CSV file has been uploaded to the database successfully."
                except IntegrityError:
                    message = "This data is already in the database."
        flash(message)
    return render_template('index.html')


@app.route('/api/departments', defaults={'limit': -1, 'offset': 0})
@app.route('/api/departments/<offset>/<limit>', methods=['GET'])
def get_departments(offset, limit):
    data = get_data('departments', offset, limit)
    records = []
    for row in data:
        records.append({'id': row[0], 'department': row[1]})
    return records


@app.route('/api/employees', defaults={'limit': -1, 'offset': 0})
@app.route('/api/employees/<offset>/<limit>', methods=['GET'])
def get_hired_employees(offset, limit):
    data = get_data('employees', offset, limit)
    records = []
    for row in data:
        records.append({
            'id': row[0], 
            'name': row[1], 
            'datetime': row[2], 
            'department_id': row[3], 
            'job_id': row[4]})
    return records


@app.route('/api/jobs', defaults={'limit': -1, 'offset': 0})
@app.route('/api/jobs/<offset>/<limit>', methods=['GET'])
def get_jobs(offset, limit):
    data = get_data('jobs', offset, limit)
    records = []
    for row in data:
        records.append({'id': row[0], 'job': row[1]})
    return records


@app.route('/api/departments/backup', methods=['GET'])
def backup_departments():
    with open('data/departments.avro', 'wb') as file:
        writer(file, schema_d, get_departments())
    return send_file('data/departments.avro')


@app.route('/api/employees/backup', methods=['GET'])
def backup_hired_employees():
    with open('data/employees.avro', 'wb') as file:
        writer(file, schema_e, get_hired_employees())
    return send_file('data/employees.avro')


@app.route('/api/jobs/backup', methods=['GET'])
def backup_jobs():
    with open('data/jobs.avro', 'wb') as file:
        writer(file, schema_j, get_jobs())
    return send_file('data/jobs.avro')


@app.route('/api/departments/restore')
def restore_departments():
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM departments;")
    data = json.loads(read_avro('departments'))
    columns = ['id', 'department']
    for row in data:
        keys = tuple(row[c] for c in columns)
        try:
            cur.execute("INSERT INTO departments VALUES (?,?);", keys)
        except IntegrityError:
            message = "Table not empty."
        print(f"Row id: {row['id']} inserted succesfully!")
    message = "Table departments restored successfully."
    flash(message)
    return redirect(('/'))


@app.route('/api/employees/restore', methods=['GET'])
def restore_employees():
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM employees;")
    data = json.loads(read_avro('employees'))
    columns = ['id', 'department', 'datetime', 'department_id', 'job_id']
    for row in data:
        keys = tuple(row[c] for c in columns)
        try:
            cur.execute("INSERT INTO employees VALUES (?,?,?,?,?);", keys)
        except IntegrityError:
            message = "Table not empty."
        print(f"Row id: {row['id']} inserted succesfully!")
    message = "Table employees restored successfully."
    flash(message)
    return redirect(('/'))


@app.route('/api/jobs/restore', methods=['GET'])
def restore_jobs():
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM jobs;")
    data = json.loads(read_avro('jobs'))
    columns = ['id', 'job']
    for row in data:
        keys = tuple(row[c] for c in columns)
        try:
            cur.execute("INSERT INTO jobs VALUES (?,?);", keys)
        except IntegrityError:
            message = "Table not empty."
        print(f"Row id: {row['id']} inserted succesfully!")
    message = "Table jobs restored successfully."
    flash(message)
    return redirect(('/'))


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)