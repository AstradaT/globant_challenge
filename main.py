from flask import Flask, jsonify, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'data'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# departments = pd.read_csv('data/raw/departments.csv', names=['id','department'], header=None).to_json()
# hired_employees = pd.read_csv('data/raw/hired_employees.csv', names=['id','name','datetime','department_id','job_id'], header=None).to_json()
# jobs = pd.read_csv('data/raw/jobs.csv', names=['id','job'], header=None).to_json()


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


with app.app_context():
    db.create_all()


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
            with db.engine.begin() as connection:
                table = file.filename
                df.to_sql(table, con=connection, if_exists='replace', index=False, chunksize=1000)
                table_2 = table.removeprefix('hired_').removesuffix('.csv')
                connection.execute(f"INSERT INTO {table_2} SELECT * FROM `{table}`;")
        success_message = "The CSV file has been uploaded to the database successfully."
        flash(success_message)
            
    return render_template('index.html')


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