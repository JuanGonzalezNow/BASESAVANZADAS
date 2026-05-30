from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()
def create_app(env='default'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)

    from app.controllers.main_controller import main_bp
    from app.controllers.moto_controller import moto_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(moto_bp)

    return app
