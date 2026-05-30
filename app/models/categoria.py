from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria     = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    nombre_categoria = db.Column(db.String(50), nullable=False)