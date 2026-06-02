from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name='development'):
    app = Flask(__name__)

    from app.config import config_dict
    app.config.from_object(config_dict[config_name])

    db.init_app(app)

    # Import models terlebih dahulu
    from app import models

    # Register blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.targets import targets_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(targets_bp)

    # Baru buat tabel
    with app.app_context():
        db.create_all()

    return app