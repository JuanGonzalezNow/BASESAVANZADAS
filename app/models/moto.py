from app import db

class Motocicleta(db.Model):
    __tablename__ = 'motocicletas'

    id_moto             = db.Column(db.Integer,       primary_key=True, autoincrement=True)
    modelo              = db.Column(db.String(100),   nullable=False)
    anio                = db.Column(db.SmallInteger,  nullable=False)
    precio_venta        = db.Column(db.Numeric(12,2), nullable=False)
    stock_disponible    = db.Column(db.Integer,       nullable=False, default=0)
    descripcion_tecnica = db.Column(db.String(500))
    url_imagen          = db.Column(db.String(255))
    id_marca            = db.Column(db.Integer, db.ForeignKey('marcas.id_marca', ondelete='SET NULL', onupdate='CASCADE'))
    id_categoria        = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria', ondelete='SET NULL', onupdate='CASCADE'))

    marca               = db.relationship('Marca')
    categoria           = db.relationship('Categoria')
