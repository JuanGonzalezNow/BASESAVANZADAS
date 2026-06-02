from functools import wraps
from flask import request, session, jsonify, redirect, url_for
from app.models.usuario import Usuario


def _admin_error(message, status_code):
    wants_json = (
        request.method != 'GET'
        or request.path.endswith('/api')
        or request.accept_mimetypes.best == 'application/json'
    )

    if wants_json:
        return jsonify({'success': False, 'message': message}), status_code

    return redirect(url_for('main.home'))

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            return _admin_error('Debes iniciar sesion para acceder al administrador', 401)

        usuario = Usuario.query.get(session['id_usuario'])
        if not usuario or usuario.id_rol != 2:
            return _admin_error('Acceso denegado. Solo administradores', 403)

        return f(*args, **kwargs)
    return decorated_function
