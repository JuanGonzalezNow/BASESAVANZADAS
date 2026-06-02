from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tipo_documento = db.Column(db.Integer, db.ForeignKey('tipos_documento.id_tipo_documento', ondelete='SET NULL', onupdate='CASCADE'))
    numero_documento = db.Column(db.String(20), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.BigInteger)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol', ondelete='SET NULL', onupdate='CASCADE'))

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)
