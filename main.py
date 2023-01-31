from flask import Flask, jsonify, request, render_template, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from sqlalchemy.exc import IntegrityError
from helpers import get_data
from fastavro import writer, schema


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
    data = get_data('departments')
    lis = []
    for row in data:
        lis.append({'id': row[0], 'department': row[1]})
    return f"{lis}"


@app.route('/api/employees', methods=['GET'])
def get_hired_employees():
    data = get_data('employees')
    lis = []
    for row in data:
        lis.append({
            'id': row[0], 
            'name': row[1], 
            'datetime': row[2], 
            'department_id': row[3], 
            'job_id': row[4]})
    return f"{lis}"


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    data = get_data('jobs')
    lis = []
    for row in data:
        lis.append({'id': row[0], 'job': row[1]})
    return f"{lis}"


@app.route('/api/departments/backup', methods=['GET'])
def backup_departments():
    data = get_data('departments')
    json = jsonify(data)
    with open('departments.avro', 'wb') as file:
        writer(file, schema, json)
    return send_file('data/avro/departments.avro', as_attachment=True)


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