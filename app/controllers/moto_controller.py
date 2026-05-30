from flask import Blueprint, render_template
from app import db
from app.models.moto import Motocicleta
from app.models.marca import Marca
from app.models.categoria import Categoria

moto_bp = Blueprint('motos', __name__)

@moto_bp.route('/motos')
def catalogo():
    # 1. Obligamos a la sesión a cerrarse y refrescar los datos externos
    db.session.commit() 

    # 2. Ahora sí hacemos la consulta limpia
    motos = Motocicleta.query.all()

    # Agrega marca y categoria a cada moto manualmente
    for moto in motos:
        moto.marca_nombre     = Marca.query.get(moto.id_marca).nombre_marca if moto.id_marca else 'Sin marca'
        moto.categoria_nombre = Categoria.query.get(moto.id_categoria).nombre_categoria if moto.id_categoria else 'Sin categoría'

    print(f"Motos encontradas: {len(motos)}")
    return render_template('motos/catalogo.html', motos=motos)