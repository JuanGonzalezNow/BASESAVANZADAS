import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'root')

    # Datos exactos de tu MySQL Workbench
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = 'root' # ← DEBES PONER TU CONTRASEÑA AQUÍ
    MYSQL_HOST     = '127.0.0.1'
    MYSQL_PORT     = '3306'
    MYSQL_DB = 'rideaxis_db' # Nombre de la base de datos de Workbench

    # URI de conexión para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default':     DevelopmentConfig
}