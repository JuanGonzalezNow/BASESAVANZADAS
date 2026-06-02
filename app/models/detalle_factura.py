from app import db
from datetime import datetime

class DetalleFactura(db.Model):
    __tablename__ = 'detalles_factura'

    id_detalle_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('facturas.id_factura', ondelete='CASCADE', onupdate='CASCADE'))
    id_moto = db.Column(db.Integer, db.ForeignKey('motocicletas.id_moto', ondelete='SET NULL', onupdate='CASCADE'))
    cantidad_vendida = db.Column(db.Integer, nullable=False)
    precio_unitario_historico = db.Column(db.Numeric(12, 2), nullable=False)

    moto = db.relationship('Motocicleta')
