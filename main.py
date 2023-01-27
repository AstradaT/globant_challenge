from flask import Flask, jsonify, request, render_template
import pandas as pd
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


departments = pd.read_csv('data/departments.csv', names=['id','department'], header=None).to_json()
hired_employees = pd.read_csv('data/hired_employees.csv', names=['id','name','datetime','department_id','job_id'], header=None).to_json()
jobs = pd.read_csv('data/jobs.csv', names=['id','job'], header=None).to_json()


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    department = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Department(id={self.id}, department={self.department})>"

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
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


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return render_template('asd.html')


@app.route('/departments', methods=['GET'])
def get_departments():
    return jsonify(departments)


@app.route('/employees', methods=['GET'])
def get_hired_employees():
    return jsonify(hired_employees)


@app.route('/jobs', methods=['GET'])
def get_jobs():
    return jsonify(jobs)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)