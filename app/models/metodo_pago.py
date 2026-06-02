from app import db

class MetodoPago(db.Model):
    __tablename__ = 'metodos_pago'

    id_metodo_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_metodo = db.Column(db.String(50), nullable=False)
