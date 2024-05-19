from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .tabelas import Usuarios

class FormularioRegistro(FlaskForm):
    user = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    ra = StringField('RA', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    # todo confirmar senha
    submit = SubmitField('Registrar')

    def validar_email(self, email):
        usuario = Usuarios.query.filter_by(email=email).first()
        if usuario:
            raise ValueError('Email já cadastrado!')
    
class FormularioLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')