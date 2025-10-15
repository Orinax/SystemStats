from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sysinfo.db'
db = SQLAlchemy(app)

class SystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(120))
    os = db.Column(db.String(120))
    cpu = db.Column(db.String(120))
    ram = db.Column(db.String(120))
    raw_json = db.Column(db.Text)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit():
