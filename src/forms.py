from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, EqualTo


class AddUser(FlaskForm):
    login      = StringField('Login', validators=[DataRequired()])
    passwowrd  = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm',message="Los Passwords deben ser iguales.")])
    confirm    = PasswordField('Confirmar Password')
    nombres    = StringField('Nombres', validators=[DataRequired()])
    apellidos  = StringField('Apellidos', validators=[DataRequired()])
    CI         = StringField('CI', validators=[DataRequired()])
    localPhone = StringField('Telefono Local')
    cellPhone  = StringField('Telefono Celular')
    dir1       = StringField('Direccion 1:')
    dir2       = StringField('Direccion 2:')