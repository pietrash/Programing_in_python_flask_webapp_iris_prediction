from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import DatabaseError

from prediction import predict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/db'
db = SQLAlchemy(app)


class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, CheckConstraint('sepal_length > 0'))
    sepal_width = db.Column(db.Float, CheckConstraint('sepal_width > 0'))
    petal_length = db.Column(db.Float, CheckConstraint('petal_length > 0'))
    petal_width = db.Column(db.Float, CheckConstraint('petal_width > 0'))
    species = db.Column(db.Integer, CheckConstraint('species IN (0, 1, 2)'))
    # Species:
    # 0 - setosa
    # 1 - versicolor
    # 2 - virginica


@app.route("/")
def home():
    data_points = DataPoint.query.all()
    return render_template('home.html', data_points=data_points)


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'GET':
        return render_template('add.html')

    try:
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        species = int(request.form['species'])

        new_data_point = DataPoint(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
            species=species
        )

        db.session.add(new_data_point)
        db.session.commit()

        return redirect('/')

    except ValueError:
        return render_template('400_error.html'), 400
    except DatabaseError:
        return render_template('400_error.html'), 400


@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_data(record_id):
    data_point = DataPoint.query.get(record_id)
    if data_point:
        db.session.delete(data_point)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('404_error.html'), 404


@app.route('/predict', methods=['GET', 'POST'])
def predict_category():
    if request.method == 'GET':
        return render_template('prediction_form.html')

    try:
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        if sepal_length < 0 or sepal_width < 0 or petal_length < 0 or petal_width < 0:
            return render_template('400_error.html'), 400

        data_points = DataPoint.query.all()
        prediction = predict(sepal_length, sepal_width, petal_length, petal_width, data_points)

        return render_template('prediction_result.html', prediction=int(prediction[0]))

    except ValueError:
        return render_template('400_error.html'), 400


# API
@app.route('/api/data', methods=['GET'])
def get_data_api():
    data_points = DataPoint.query.all()
    data_list = [{
        'id': data.id,
        'sepal_length': data.sepal_length,
        'sepal_width': data.sepal_width,
        'petal_length': data.petal_length,
        'petal_width': data.petal_width,
        'species': data.species
    } for data in data_points]

    return jsonify(data_list)


@app.route('/api/data', methods=['POST'])
def add_data_api():
    try:
        data_json = request.get_json()

        sepal_length = float(data_json['sepal_length'])
        sepal_width = float(data_json['sepal_width'])
        petal_length = float(data_json['petal_length'])
        petal_width = float(data_json['petal_width'])
        species = int(data_json['species'])

        new_data_point = DataPoint(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
            species=species
        )

        db.session.add(new_data_point)
        db.session.commit()

        return jsonify({'id': new_data_point.id}), 201

    except ValueError:
        return jsonify({'error': 'Invalid data'}), 400
    except DatabaseError:
        return jsonify({'error': 'Invalid data'}), 400


@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_data_api(record_id):
    data_point = DataPoint.query.get(record_id)
    if data_point:
        db.session.delete(data_point)
        db.session.commit()
        return jsonify({'id': record_id})
    else:
        return jsonify({'error': 'Record not found'}), 404


@app.route('/api/predictions', methods=['GET'])
def api_predict_category():
    try:
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))

        if sepal_length < 0 or sepal_width < 0 or petal_length < 0 or petal_width < 0:
            return jsonify({'error': 'Invalid data'}), 400

        data_points = DataPoint.query.all()

        prediction = predict(sepal_length, sepal_width, petal_length, petal_width, data_points)

        return jsonify({'predicted_category': str(prediction[0])})

    except ValueError:
        return jsonify({'error': 'Invalid data'}), 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
