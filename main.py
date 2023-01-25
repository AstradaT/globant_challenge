from flask import Flask, jsonify
from flask import request
import pandas as pd


app = Flask(__name__)


departments = pd.read_csv('data/departments.csv').to_json()
hired_employees = pd.read_csv('data/hired_employees.csv').to_json()
jobs = pd.read_csv('data/jobs.csv').to_json()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Globant Data Challenge</h1>'''


@app.route('/departments', methods=['GET'])
def departments():
    return jsonify(departments)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)