from main import db


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