from flask import Flask, request, jsonify, render_template
from models import db, Record

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# create tables
with app.app_context():
    db.create_all()


# Home Page
@app.route('/')
def index():
    records = Record.query.all()
    return render_template("index.html", records=records)


# Add Record
@app.route('/add', methods=['POST'])
def add_record():
    name = request.form.get("name")

    if not name:
        return jsonify({"error": "Name required"}), 400

    record = Record(name=name)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Record added"})


# Delete Record
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    record = Record.query.get(id)

    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Record deleted"})




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)