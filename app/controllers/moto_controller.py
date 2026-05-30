from flask import Blueprint, render_template, request
from app import db
from app.models.moto import Motocicleta
from app.models.marca import Marca
from app.models.categoria import Categoria

moto_bp = Blueprint('motos', __name__)

@moto_bp.route('/motos')
def catalogo():
    db.session.commit()

    query = Motocicleta.query

    marca = request.args.get('marca')
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float, default=85000000)
    sort = request.args.get('sort', 'asc')

    if marca:
        query = query.filter_by(id_marca=marca)

    if precio_min:
        query = query.filter(Motocicleta.precio_venta >= precio_min)

    if precio_max:
        query = query.filter(Motocicleta.precio_venta <= precio_max)

    if sort == 'desc':
        query = query.order_by(Motocicleta.precio_venta.desc())
    else:
        query = query.order_by(Motocicleta.precio_venta.asc())

    motos = query.all()

    for moto in motos:
        moto.marca_nombre = Marca.query.get(moto.id_marca).nombre_marca if moto.id_marca else 'Sin marca'
        moto.categoria_nombre = Categoria.query.get(moto.id_categoria).nombre_categoria if moto.id_categoria else 'Sin categoría'

    marcas = Marca.query.all()

    return render_template('motos/catalogo.html', motos=motos, marcas=marcas,
                         marca=marca, precio_min=precio_min, precio_max=precio_max, sort=sort)