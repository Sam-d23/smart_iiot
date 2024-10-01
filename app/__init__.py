from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
migrate = Migrate()
scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.start()

    from app.controllers import main
    app.register_blueprint(main)

    return app


def simulate_data():
    with app.app_context():
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

scheduler.add_job(func=simulate_data, trigger="interval", seconds=3600)
