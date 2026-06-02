from flask import Blueprint, session, jsonify, render_template, redirect, url_for, send_file
from functools import wraps
from app import db
from app.models.moto import Motocicleta
from app.models.usuario import Usuario
from sqlalchemy import func
import datetime

carrito_bp = Blueprint('carrito', __name__)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            return jsonify({'success': False, 'message': 'Login requerido'}), 401
        return f(*args, **kwargs)
    return decorated_function

@carrito_bp.route('/carrito')
@require_login
def ver_carrito():
    carrito = session.get('carrito', [])
    motos_data = []
    total = 0

    for item in carrito:
        moto = Motocicleta.query.get(item['id_moto'])
        if moto:
            subtotal = moto.precio_venta * item['cantidad']
            motos_data.append({
                'id_moto': moto.id_moto,
                'modelo': moto.modelo,
                'precio': float(moto.precio_venta),
                'cantidad': item['cantidad'],
                'subtotal': float(subtotal),
                'url_imagen': moto.url_imagen
            })
            total += subtotal

    return jsonify({
        'success': True,
        'carrito': motos_data,
        'total': float(total),
        'total_items': len(carrito)
    })

@carrito_bp.route('/carrito/agregar', methods=['POST'])
@require_login
def agregar_carrito():
    from flask import request
    data = request.get_json()
    id_moto = data.get('id_moto')
    cantidad = data.get('cantidad', 1)

    moto = Motocicleta.query.get(id_moto)
    if not moto:
        return jsonify({'success': False, 'message': 'Motocicleta no encontrada'}), 404

    carrito = session.get('carrito', [])
    item_existente = next((item for item in carrito if item['id_moto'] == id_moto), None)

    if item_existente:
        item_existente['cantidad'] += cantidad
    else:
        carrito.append({'id_moto': id_moto, 'cantidad': cantidad})

    session['carrito'] = carrito
    session.modified = True

    return jsonify({
        'success': True,
        'message': f'{moto.modelo} agregado al carrito',
        'total_items': len(carrito)
    })

@carrito_bp.route('/carrito/eliminar', methods=['POST'])
@require_login
def eliminar_carrito():
    from flask import request
    data = request.get_json()
    id_moto = data.get('id_moto')

    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id_moto'] != id_moto]
    session['carrito'] = carrito
    session.modified = True

    return jsonify({
        'success': True,
        'message': 'Item removido del carrito',
        'total_items': len(carrito)
    })

@carrito_bp.route('/checkout', methods=['GET'])
@require_login
def checkout():
    carrito = session.get('carrito', [])

    if not carrito:
        return redirect(url_for('motos.catalogo'))

    motos_data = []
    total = 0

    for item in carrito:
        moto = Motocicleta.query.get(item['id_moto'])
        if moto:
            subtotal = moto.precio_venta * item['cantidad']
            motos_data.append({
                'id_moto': moto.id_moto,
                'modelo': moto.modelo,
                'precio': float(moto.precio_venta),
                'cantidad': item['cantidad'],
                'subtotal': float(subtotal),
                'url_imagen': moto.url_imagen
            })
            total += subtotal

    usuario = Usuario.query.get(session['id_usuario'])

    return render_template('checkout.html',
                         carrito=motos_data,
                         total=float(total),
                         usuario=usuario)

@carrito_bp.route('/checkout/procesar', methods=['POST'])
@require_login
def procesar_checkout():
    from flask import request

    carrito = session.get('carrito', [])
    if not carrito:
        return jsonify({'success': False, 'message': 'Carrito vacío'}), 400

    data = request.get_json()
    id_metodo_pago = data.get('id_metodo_pago')
    direccion = data.get('direccion', '').strip()
    ciudad = data.get('ciudad', '').strip()
    codigo_postal = data.get('codigo_postal', '').strip()

    if not id_metodo_pago:
        return jsonify({'success': False, 'message': 'Selecciona un método de pago'}), 400

    if not all([direccion, ciudad, codigo_postal]):
        return jsonify({'success': False, 'message': 'Completa todos los datos de entrega'}), 400

    usuario = Usuario.query.get(session['id_usuario'])
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 401

    # Validar stock disponible
    for item in carrito:
        moto = Motocicleta.query.get(item['id_moto'])
        if not moto:
            return jsonify({'success': False, 'message': f'Motocicleta no encontrada'}), 404
        if moto.stock_disponible < item['cantidad']:
            return jsonify({'success': False, 'message': f'Stock insuficiente para {moto.modelo}. Disponible: {moto.stock_disponible}'}), 400

    subtotal = 0
    numero_factura = f"FAC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    for item in carrito:
        moto = Motocicleta.query.get(item['id_moto'])
        if moto:
            subtotal += float(moto.precio_venta) * item['cantidad']

    iva = subtotal * 0.19
    total = subtotal + iva

    try:
        from app.models.factura import Factura
        from app.models.detalle_factura import DetalleFactura
        from app.models.entrega import Entrega

        factura = Factura(
            numero_factura=numero_factura,
            fecha_emision=datetime.datetime.now(),
            subtotal=subtotal,
            iva=iva,
            total_pagar=total,
            estado_factura='Confirmada',
            id_cliente=usuario.id_usuario,
            id_metodo_pago=id_metodo_pago
        )
        db.session.add(factura)
        db.session.flush()

        for item in carrito:
            moto = Motocicleta.query.get(item['id_moto'])
            if moto:
                detalle = DetalleFactura(
                    id_factura=factura.id_factura,
                    id_moto=moto.id_moto,
                    cantidad_vendida=item['cantidad'],
                    precio_unitario_historico=moto.precio_venta
                )
                db.session.add(detalle)

        entrega = Entrega(
            id_factura=factura.id_factura,
            direccion=direccion,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            estado_entrega='Pendiente'
        )
        db.session.add(entrega)
        db.session.commit()

        session['carrito'] = []
        session.modified = True

        return jsonify({
            'success': True,
            'message': 'Compra realizada exitosamente',
            'numero_factura': numero_factura,
            'id_factura': factura.id_factura,
            'total': float(total)
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error en checkout: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al procesar la compra: {str(e)}'
        }), 500

@carrito_bp.route('/factura/<int:id_factura>/descargar', methods=['GET'])
@require_login
def descargar_factura(id_factura):
    from app.models.factura import Factura
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from io import BytesIO

    factura = Factura.query.get(id_factura)
    if not factura:
        return jsonify({'success': False, 'message': 'Factura no encontrada'}), 404

    if factura.id_cliente != session.get('id_usuario'):
        return jsonify({'success': False, 'message': 'No tienes permiso'}), 403

    cliente = factura.id_cliente and db.session.get(Usuario, factura.id_cliente)
    entrega = factura.entregas[0] if factura.entregas else None
    detalles = factura.detalles

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()

        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=6,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )

        # Encabezado
        elements.append(Paragraph('RIDEAXIS', title_style))
        elements.append(Paragraph(f'Factura #{factura.numero_factura}', heading_style))
        elements.append(Paragraph(f'Fecha: {factura.fecha_emision.strftime("%d de %B de %Y")}', styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))

        # Información del Cliente
        elements.append(Paragraph('INFORMACIÓN DEL CLIENTE', heading_style))
        client_data = [
            ['Campo', 'Valor'],
            ['Nombre', f'{cliente.nombre} {cliente.apellido}' if cliente else 'N/A'],
            ['Email', cliente.correo_electronico if cliente else 'N/A'],
            ['Teléfono', str(cliente.telefono) if cliente and cliente.telefono else 'N/A'],
            ['Documento', cliente.numero_documento if cliente else 'N/A'],
        ]
        client_table = Table(client_data, colWidths=[2*inch, 4*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        elements.append(client_table)
        elements.append(Spacer(1, 0.2*inch))

        # Información de Entrega
        if entrega:
            elements.append(Paragraph('INFORMACIÓN DE ENTREGA', heading_style))
            delivery_data = [
                ['Dirección', entrega.direccion],
                ['Ciudad', entrega.ciudad],
                ['Código Postal', entrega.codigo_postal],
                ['Estado', entrega.estado_entrega],
            ]
            delivery_table = Table(delivery_data, colWidths=[2*inch, 4*inch])
            delivery_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
            ]))
            elements.append(delivery_table)
            elements.append(Spacer(1, 0.2*inch))

        # Detalles de Compra
        elements.append(Paragraph('DETALLES DE COMPRA', heading_style))
        details_data = [['Modelo', 'Cantidad', 'Precio Unitario', 'Subtotal']]

        for detalle in detalles:
            moto = detalle.moto
            subtotal = float(detalle.precio_unitario_historico) * detalle.cantidad_vendida
            details_data.append([
                moto.modelo if moto else 'N/A',
                str(detalle.cantidad_vendida),
                f'${float(detalle.precio_unitario_historico):,.0f}',
                f'${subtotal:,.0f}'
            ])

        details_table = Table(details_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 0.3*inch))

        # Totales
        totals_data = [
            ['', 'Subtotal', f'${float(factura.subtotal):,.0f}'],
            ['', 'IVA (19%)', f'${float(factura.iva):,.0f}'],
            ['', 'TOTAL', f'${float(factura.total_pagar):,.0f}'],
        ]
        totals_table = Table(totals_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#dc2626')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.4*inch))

        # Pie
        elements.append(Paragraph('Gracias por tu compra en RIDEAXIS', styles['Normal']))
        elements.append(Paragraph(f'Estado: {factura.estado_factura}', styles['Normal']))

        doc.build(elements)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Factura_{factura.numero_factura}.pdf'
        )
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return jsonify({'success': False, 'message': f'Error al generar PDF: {str(e)}'}), 500

@carrito_bp.route('/mis-compras')
@require_login
def mis_compras():
    from app.models.factura import Factura

    usuario = Usuario.query.get(session['id_usuario'])
    facturas = Factura.query.filter_by(id_cliente=session['id_usuario']).order_by(Factura.fecha_emision.desc()).all()

    return render_template('mis_compras.html', usuario=usuario, facturas=facturas)

@carrito_bp.route('/compra-exitosa/<int:id_factura>')
@require_login
def compra_exitosa(id_factura):
    from app.models.factura import Factura

    factura = Factura.query.get(id_factura)
    if not factura or factura.id_cliente != session.get('id_usuario'):
        return redirect(url_for('carrito.ver_carrito'))

    usuario = Usuario.query.get(factura.id_cliente)
    return render_template('compra_exitosa.html', factura=factura, usuario=usuario)
