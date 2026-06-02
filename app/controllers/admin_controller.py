from datetime import date, datetime
from decimal import Decimal

from flask import Blueprint, render_template, request, jsonify
from app import db
from app.decorators.admin_decorator import require_admin
from app.models.usuario import Usuario
from app.models.moto import Motocicleta
from app.models.factura import Factura
from app.models.marca import Marca
from app.models.categoria import Categoria
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def serializar_valor_sql(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    if isinstance(value, date):
        return value.isoformat()

    return value


def entero_o_none(value):
    if value in (None, ''):
        return None

    return int(value)

@admin_bp.route('/dashboard')
@require_admin
def dashboard():
    # Estadísticas generales
    total_usuarios = Usuario.query.count()
    total_motos = Motocicleta.query.count()
    total_ventas = Factura.query.count()

    # Ingresos totales
    ingresos_totales = db.session.query(func.sum(Factura.total_pagar)).scalar() or 0

    stats = {
        'total_usuarios': total_usuarios,
        'total_motos': total_motos,
        'total_ventas': total_ventas,
        'ingresos_totales': float(ingresos_totales)
    }

    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/motos')
@require_admin
def listar_motos():
    motos = Motocicleta.query.order_by(Motocicleta.id_moto.desc()).all()
    marcas = Marca.query.order_by(Marca.nombre_marca.asc()).all()
    categorias = Categoria.query.order_by(Categoria.nombre_categoria.asc()).all()

    marcas_por_id = {marca.id_marca: marca.nombre_marca for marca in marcas}
    categorias_por_id = {
        categoria.id_categoria: categoria.nombre_categoria
        for categoria in categorias
    }

    return render_template(
        'admin/motos.html',
        motos=motos,
        marcas=marcas,
        categorias=categorias,
        marcas_por_id=marcas_por_id,
        categorias_por_id=categorias_por_id
    )

@admin_bp.route('/motos/api', methods=['GET'])
@require_admin
def api_listar_motos():
    motos = Motocicleta.query.all()
    data = [{
        'id_moto': m.id_moto,
        'modelo': m.modelo,
        'anio': m.anio,
        'precio_venta': float(m.precio_venta),
        'stock_disponible': m.stock_disponible,
        'descripcion_tecnica': m.descripcion_tecnica,
        'url_imagen': m.url_imagen,
        'id_marca': m.id_marca,
        'id_categoria': m.id_categoria
    } for m in motos]
    return jsonify({'success': True, 'motos': data})

@admin_bp.route('/motos/crear', methods=['POST'])
@require_admin
def crear_moto():
    data = request.get_json()

    try:
        moto = Motocicleta(
            modelo=data.get('modelo'),
            anio=data.get('anio'),
            precio_venta=float(data.get('precio_venta', 0)),
            stock_disponible=int(data.get('stock_disponible', 0)),
            descripcion_tecnica=data.get('descripcion_tecnica', ''),
            url_imagen=data.get('url_imagen', ''),
            id_marca=entero_o_none(data.get('id_marca')),
            id_categoria=entero_o_none(data.get('id_categoria'))
        )
        db.session.add(moto)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Moto creada exitosamente', 'id_moto': moto.id_moto})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@admin_bp.route('/motos/<int:id_moto>/editar', methods=['POST'])
@require_admin
def editar_moto(id_moto):
    moto = Motocicleta.query.get(id_moto)
    if not moto:
        return jsonify({'success': False, 'message': 'Moto no encontrada'}), 404

    data = request.get_json()

    try:
        moto.modelo = data.get('modelo', moto.modelo)
        moto.anio = data.get('anio', moto.anio)
        moto.precio_venta = float(data.get('precio_venta', moto.precio_venta))
        moto.stock_disponible = int(data.get('stock_disponible', moto.stock_disponible))
        moto.descripcion_tecnica = data.get('descripcion_tecnica', moto.descripcion_tecnica)
        moto.url_imagen = data.get('url_imagen', moto.url_imagen)
        moto.id_marca = entero_o_none(data.get('id_marca', moto.id_marca))
        moto.id_categoria = entero_o_none(data.get('id_categoria', moto.id_categoria))

        db.session.commit()
        return jsonify({'success': True, 'message': 'Moto actualizada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@admin_bp.route('/motos/<int:id_moto>/eliminar', methods=['POST'])
@require_admin
def eliminar_moto(id_moto):
    moto = Motocicleta.query.get(id_moto)
    if not moto:
        return jsonify({'success': False, 'message': 'Moto no encontrada'}), 404

    try:
        db.session.delete(moto)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Moto eliminada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@admin_bp.route('/ventas')
@require_admin
def ventas():
    # Obtener todas las ventas
    from app.models.detalle_factura import DetalleFactura

    ventas = Factura.query.order_by(Factura.fecha_emision.desc()).all()

    return render_template('admin/ventas.html', ventas=ventas)

@admin_bp.route('/usuarios')
@require_admin
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuarios/api', methods=['GET'])
@require_admin
def api_usuarios():
    usuarios = Usuario.query.all()
    data = [{
        'id_usuario': u.id_usuario,
        'nombre': u.nombre,
        'apellido': u.apellido,
        'correo_electronico': u.correo_electronico,
        'telefono': u.telefono,
        'numero_documento': u.numero_documento
    } for u in usuarios]
    return jsonify({'success': True, 'usuarios': data})

@admin_bp.route('/sql', methods=['GET', 'POST'])
@require_admin
def ejecutor_sql():
    if request.method == 'GET':
        return render_template('admin/sql.html')

    # POST - Ejecutar SQL
    try:
        data = request.get_json()
        query = data.get('query', '').strip() if data else ''

        if not query:
            return jsonify({'success': False, 'message': 'Query vacío'}), 400

        query_upper = query.upper()

        if not query_upper.startswith('SELECT'):
            return jsonify({'success': False, 'message': 'Solo SELECT'}), 400

        if any(x in query_upper for x in ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER']):
            return jsonify({'success': False, 'message': 'Comando no permitido'}), 400

        from sqlalchemy import text
        resultado = db.session.execute(text(query))
        columnas = list(resultado.keys())
        filas = [
            {columna: serializar_valor_sql(valor) for columna, valor in zip(columnas, row)}
            for row in resultado.fetchall()
        ]

        return jsonify({
            'success': True,
            'columns': columnas,
            'rows': filas,
            'count': len(filas)
        })

    except Exception as e:
        print(f"Error SQL: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400
