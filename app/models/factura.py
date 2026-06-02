from app import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'

    id_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_factura = db.Column(db.String(50), nullable=False, unique=True)
    fecha_emision = db.Column(db.DateTime, default=datetime.now)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)
    iva = db.Column(db.Numeric(12, 2), nullable=False)
    total_pagar = db.Column(db.Numeric(12, 2), nullable=False)
    estado_factura = db.Column(db.String(30), default='Pendiente')
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='SET NULL', onupdate='CASCADE'))
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodos_pago.id_metodo_pago', ondelete='SET NULL', onupdate='CASCADE'))

    detalles = db.relationship('DetalleFactura', backref='factura', cascade='all, delete-orphan')
