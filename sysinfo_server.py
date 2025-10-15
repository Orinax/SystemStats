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

@app.before_request
def create_tables():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(force=True)
    sysinfo = SystemInfo(
        hostname=data.get('hostname', ''),
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
       'hostname': info.hostname,
       'os': info.os,
       'cpu': info.cpu,
       'ram': info.ram,
    } for info in infos])


if __name__ == '__main__':
    app.run(port=5000)
