from app import db
from datetime import datetime

class Entrega(db.Model):
    __tablename__ = 'entregas'

    id_entrega = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('facturas.id_factura', ondelete='CASCADE', onupdate='CASCADE'))
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    estado_entrega = db.Column(db.String(30), default='Pendiente')

    factura = db.relationship('Factura', backref='entregas')
