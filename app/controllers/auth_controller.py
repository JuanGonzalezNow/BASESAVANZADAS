from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.usuario import Usuario
from app.forms.forms import RegistroForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/registro', methods=['POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        usuario = Usuario(
            nombre=form.nombre.data.lower(),
            apellido=form.apellido.data.lower(),
            telefono=int(form.telefono.data),
            id_tipo_documento=int(form.id_tipo_documento.data),
            numero_documento=form.numero_documento.data,
            correo_electronico=form.correo_electronico.data.lower(),
            id_rol=1
        )
        usuario.set_password(form.contrasena_hash.data)

        try:
            db.session.add(usuario)
            db.session.commit()
            return jsonify({
                'success': True,
                'nombre': usuario.nombre.capitalize(),  # ← AGREGA ESTO para el toast
                'message': '¡Cuenta creada exitosamente! Por favor inicia sesión.'
            })
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR registro] {e}")  # ← solo en consola, NO al navegador
            return jsonify({
                'success': False,
                'message': 'Error interno al crear la cuenta. Intenta de nuevo.'  # ← mensaje genérico
            }), 500  # ← cambia 400 por 500 para errores internos
    else:
        errores = {field: errors[0] for field, errors in form.errors.items()}
        return jsonify({
            'success': False,
            'errors': errores
        }), 400


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
            correo_electronico=form.correo_electronico.data.lower()
        ).first()

        if usuario and usuario.check_password(form.contrasena_hash.data):
            session['id_usuario'] = usuario.id_usuario
            session['nombre_usuario'] = usuario.nombre
            session['correo_electronico'] = usuario.correo_electronico
            session['id_rol'] = usuario.id_rol

            return jsonify({
                'success': True,
                'message': f'¡Bienvenido {usuario.nombre.capitalize()}!',
                'id_rol': usuario.id_rol,
                'es_admin': usuario.id_rol == 2
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Correo o contraseña incorrectos'
            }), 401
    else:
        errores = {field: errors[0] for field, errors in form.errors.items()}
        return jsonify({
            'success': False,
            'errors': errores
        }), 400


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))