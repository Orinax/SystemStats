from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sysinfo.db'
db = SQLAlchemy(app)


class SystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.Text)
    memory = db.Column(db.Text)
    network = db.Column(db.Text)
    cpu = db.Column(db.Text)
    graphics = db.Column(db.Text)
    machine = db.Column(db.Text)
    drives = db.Column(db.Text)
    raw_json = db.Column(db.Text)

# Create tables on startup
with app.app_context():
    db.create_all()


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(force=True)

    system_info = data.get('system', {})
    memory_info = data.get('memory', {})
    network_info = data.get('network', {})
    cpu_info = data.get('cpu', {})
    graphics_info = data.get('graphics', {})
    machine_info = data.get('machine', {})
    drives_info = data.get('drives', {})

    sysinfo = SystemInfo(
        os=data.get('distro', {}).get('name', '') + " " + data.get('distro', {}).get('version', ''),
        cpu=data.get('cpu', {}).get('model', ''),
        ram=str(data.get('memory', {}).get('total', '')),
        raw_json=json.dumps(data)
    )
    db.session.add(sysinfo)
    db.session.commit()
    return jsonify({'status': 'success', 'id': sysinfo.id})

@app.route('/list', methods=['GET'])
def list_infos():
    infos = SystemInfo.query.all()
    return jsonify([{
       'id': info.id,
       'os': info.os,
       'cpu': info.cpu,
       'ram': info.ram,
    } for info in infos])


if __name__ == '__main__':
    app.run(port=5000)
