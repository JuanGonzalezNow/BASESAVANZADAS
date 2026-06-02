from app import db

class TipoDocumento(db.Model):
    __tablename__ = 'tipos_documento'

    id_tipo_documento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_tipo = db.Column(db.String(50), nullable=False, unique=True)
