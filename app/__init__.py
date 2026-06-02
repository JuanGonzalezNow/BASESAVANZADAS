from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config


db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(env='default'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    csrf.init_app(app)

    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)

    from app.controllers.main_controller import main_bp
    from app.controllers.moto_controller import moto_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.carrito_controller import carrito_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(moto_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(carrito_bp)
    app.register_blueprint(admin_bp)

    return app