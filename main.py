from flask import Flask, jsonify, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import sqlite3
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


@app.route('/api/departments', methods=['GET'])
def get_departments():
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM departments;").fetchall()
    lis = []
    for row in result:
        lis.append({'id': row[0], 'department': row[1]})
    return f"{lis}"


@app.route('/api/employees', methods=['GET'])
def get_hired_employees():
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM employees;").fetchall()
    lis = []
    for row in result:
        lis.append({
            'id': row[0], 
            'name': row[1], 
            'datetime': row[2], 
            'department_id': row[3], 
            'job_id': row[4]})
    return f"{lis}"


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM jobs;").fetchall()
    lis = []
    for row in result:
        lis.append({'id': row[0], 'job': row[1]})
    return f"{lis}"


@app.route('/api/departments/backup', methods=['GET'])
def backup_departments():
    pass


@app.route('/api/employees/backup', methods=['GET'])
def backup_hired_employees():
    pass


@app.route('/api/jobs/backup', methods=['GET'])
def backup_jobs():
    pass


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)