from app import db

class Marca(db.Model):
    __tablename__ = 'marcas'
    id_marca     = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    nombre_marca = db.Column(db.String(50), nullable=False)