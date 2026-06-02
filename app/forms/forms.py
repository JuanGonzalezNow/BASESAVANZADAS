from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp
from app.models.usuario import Usuario
import re

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre',
        validators=[
            DataRequired(message='El nombre es requerido'),
            Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres'),
            Regexp(r'^[a-záéíóúñ\s]+$', flags=re.IGNORECASE, message='Solo se aceptan letras')
        ])

    apellido = StringField('Apellido',
        validators=[
            DataRequired(message='El apellido es requerido'),
            Length(min=2, max=100, message='El apellido debe tener entre 2 y 100 caracteres'),
            Regexp(r'^[a-záéíóúñ\s]+$', flags=re.IGNORECASE, message='Solo se aceptan letras')
        ])

    telefono = StringField('Teléfono',
        validators=[
            DataRequired(message='El teléfono es requerido'),
            Regexp(r'^\d{10}$', message='Solo se aceptan 10 dígitos sin símbolos')
        ])

    id_tipo_documento = SelectField('Tipo de Documento',
        choices=[
            ('1', 'Cédula de Ciudadanía (CC)'),
            ('2', 'Tarjeta de Identidad (TI)'),
            ('3', 'Cédula de Extranjería (CE)')
        ],
        validators=[DataRequired(message='Selecciona un tipo de documento')])

    numero_documento = StringField('Número de Documento',
        validators=[
            DataRequired(message='El número de documento es requerido'),
            Regexp(r'^\d+$', message='Solo se aceptan números')
        ])

    correo_electronico = StringField('Correo Electrónico',
        validators=[
            DataRequired(message='El correo es requerido'),
            Email(message='Ingresa un correo válido (ejemplo@correo.com)')
        ])

    contrasena_hash = PasswordField('Contraseña',
        validators=[
            DataRequired(message='La contraseña es requerida'),
            Length(min=8, max=16, message='La contraseña debe tener entre 8 y 16 caracteres'),
            Regexp(r'^[a-zA-Z0-9]+$', message='La contraseña solo acepta letras (mayúsculas/minúsculas) y números, sin símbolos')
        ])

    submit = SubmitField('Crear Cuenta')

    def validate_correo_electronico(self, correo_electronico):
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico.data).first()
        if usuario:
            raise ValidationError('Este correo ya está registrado')

    def validate_telefono(self, telefono):
        usuario = Usuario.query.filter_by(telefono=telefono.data).first()
        if usuario:
            raise ValidationError('Este teléfono ya está registrado')

    def validate_numero_documento(self, numero_documento):
        usuario = Usuario.query.filter_by(numero_documento=numero_documento.data).first()
        if usuario:
            raise ValidationError('Este documento ya está registrado')


class LoginForm(FlaskForm):
    correo_electronico = StringField('Correo Electrónico',
        validators=[
            DataRequired(message='El correo es requerido'),
            Email(message='Ingresa un correo válido')
        ])

    contrasena_hash = PasswordField('Contraseña',
        validators=[DataRequired(message='La contraseña es requerida')])

    submit = SubmitField('Ingresar')

    def validate_correo_electronico(self, correo_electronico):
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico.data).first()
        if not usuario:
            raise ValidationError('Correo o contraseña incorrectos')

