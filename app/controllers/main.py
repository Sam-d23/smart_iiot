import random
from flask import Blueprint, jsonify, request
from app.models.sensor import Sensor, SensorData
from app import db


main = Blueprint('main', __name__)


@main.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([sensor.name for sensor in sensors])


@main.route('/sensors/<int:sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    data = SensorData.query.filter_by(sensor_id=sensor_id).all()
    return jsonify(
            [{'temperature': d.temperature, 'timestamp': d.timestamp}
             for d in data])


@main.route('/data/generate', methods=['POST'])
def generate_data():
    sensors = Sensor.query.all()
    for sensor in sensors:
        data = SensorData(
            sensor_id=sensor.id,
            temperature=random.uniform(20, 30),
            pressure=random.uniform(900, 1100),
            vibration=random.uniform(0.1, 1.5)
        )
        db.session.add(data)
    db.session.commit()
    return jsonify({'message': 'Data generated successfully!'})
