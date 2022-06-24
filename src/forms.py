from ctypes import Union
from datetime import date
from typing import Dict, List, Union
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, TextAreaField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired, EqualTo, StopValidation, InputRequired
from src.DB_Model import Cosecha, Persona, TipoProductor, Users,Groups
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
    groups     = SelectField('Grupos',choices=list(map(lambda g: g.group,Groups.query.all())) + [""] )


class ModifyUserForm(FlaskForm):
    login      = StringField('Login', validators=[InputRequired()],description="No debe existir, Obligatorio*",render_kw={'readonly':'readonly'})
    name       = StringField('Nombres', validators=[InputRequired()],description="Obligatorio*")
    surname    = StringField('Apellidos', validators=[InputRequired()],description="Obligatorio*")
    group_user   = SelectField('Grupos',choices=list(map(lambda g: g.group,Groups.query.all())) + [""] )
    cosecha_user = SelectField('Cosechas',choices=Cosecha.query.all() + [""] )


class ModifyUserFormParser():

    months : Dict[str,int] = {
        "Ene":1,
        "Feb":2,
        "Mar":3,
        "Abr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Ago":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dic":12
    }

    @staticmethod
    def parseLogin(login : str) -> str:
        return login

    @staticmethod
    def parseName(name : str) -> str:
        return name
    
    @staticmethod
    def parseSurname(surname : str) -> str:
        return surname
    
    @staticmethod
    def parseGroup(groupName : Union[str,None]) -> List[Groups]:
        if groupName is None or groupName == "":
            return []
        g = Groups.query.filter_by(group=groupName).first()
        if (g and g is not None):
            return [g]
        else:
            return []

    @staticmethod
    def parseDate(dt : Union[str,None]) -> List[Cosecha]:
        if dt is None or dt == "":
            return []
        (_,m1,_,m2,y) = dt.split(sep=" ")
        m1_ = ModifyUserFormParser.months[m1]
        m2_ = ModifyUserFormParser.months[m2]
        y2_ = int(y)
        if (m1_ >= m2_):
            y1_ = y2_-1
        else:
            y1_ = y2_
        
        d1 = date(y1_,m1_,1)
        d2 = date(y2_,m2_,1)
        return Cosecha.query.filter_by(start_date=d1,end_date=d2).all()

def validate_Person(form, field):
    if (Persona.query.filter_by(CI = field.data).first() is not None):
        print(f"\n\n\nFIELD IS: {field}\n\n\n")
        print(f"\n\n\nFIELD.DATA IS: {field.data}\n\n\n")
        raise ValidationError("El usuario pertenece ya al sistema.")

class AddProducerForm(FlaskForm):
    CI                  = StringField('Cedula', validators=[InputRequired(),validate_Person],description="No debe existir, Obligatorio*")
    surname             = StringField('Apellidos', validators=[InputRequired()])
    name                = StringField('Nombres', validators=[InputRequired()])
    localPhone          = StringField('Telefono local', validators=[InputRequired()])
    cellPhone           = StringField('Telefono celular', validators=[InputRequired()],description="Obligatorio*")
    persona_productor   = SelectField('Tipo de productor', choices=list(map(lambda tp: tp.description,TipoProductor.query.all())) + [""] )
    dir1                = StringField('Direccion 1', validators=[InputRequired()],description="Obligatorio*")
    dir2                = StringField('Direccion 2', validators=[InputRequired()],description="Obligatorio*")

def validate_Description(form, field):
    if (TipoProductor.query.filter_by(description = field.data).first() is not None):
        print(f"\n\n\nFIELD IS: {field}\n\n\n")
        print(f"\n\n\nFIELD.DATA IS: {field.data}\n\n\n")
        raise ValidationError("El usuario pertenece ya al sistema.")

class AddTypeOfProducer(FlaskForm):
    ID          = StringField('ID', validators=[InputRequired()],description="No debe existir, Obligatorio*")
    description = StringField('description', validators=[InputRequired(),validate_Description])
