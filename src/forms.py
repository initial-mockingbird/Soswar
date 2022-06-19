from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, TextAreaField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired, EqualTo, StopValidation, InputRequired
from src.DB_Model import Cosecha, Users,Groups
from flask import flash

def validate_login(form, field):
    if (Users.query.filter_by(login = field.data).first() is not None):
        print(f"\n\n\nFIELD IS: {field}\n\n\n")
        print(f"\n\n\nFIELD.DATA IS: {field.data}\n\n\n")
        raise ValidationError("El usuario pertenece ya al sistema.")

class AddUserForm(FlaskForm):
    login      = StringField('Login', validators=[InputRequired(),validate_login],description="No debe existir, Obligatorio*")
    password   = PasswordField('Password', validators=[InputRequired(),EqualTo('confirm',message="Los Passwords deben ser iguales.")])
    confirm    = PasswordField('Confirmar Password')
    nombres    = StringField('Nombres', validators=[InputRequired()],description="Obligatorio*")
    apellidos  = StringField('Apellidos', validators=[InputRequired()],description="Obligatorio*")
    groups     = SelectMultipleField('Groups',option_widget=widgets.CheckboxInput(),choices=Groups.query.all(),widget=widgets.ListWidget(prefix_label=False) )


class ModifyUserForm(FlaskForm):
    login      = StringField('Login', validators=[InputRequired(),validate_login],description="No debe existir, Obligatorio*",render_kw={'disabled':'disabled'})
    name       = StringField('Nombres', validators=[InputRequired()],description="Obligatorio*")
    surname    = StringField('Apellidos', validators=[InputRequired()],description="Obligatorio*")
    group_user = SelectField('Grupos',choices=Groups.query.all() )
    cosecha_user = SelectField('Cosechas',choices=Cosecha.query.all() )

    