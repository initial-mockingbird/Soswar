from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, StopValidation, InputRequired, NumberRange, ValidationError
from src.DB_Model import Cosecha,Compra, Persona, TipoProductor, Users,Groups
import re
from src.PORM import CosechaControlAPI, UserControlAPI, UserViewAPI
from init import ActiveApp
from datetime import date 

'''
def validate_login(form, field):
    if (Users.query.filter_by(login = field.data).first() is not None):
        print(f"\n\n\nFIELD IS: {field}\n\n\n")
        print(f"\n\n\nFIELD.DATA IS: {field.data}\n\n\n")
        form.login.errors += (ValidationError("El usuario pertenece ya al sistema."),)
        raise ValidationError("El usuario pertenece ya al sistema.")
'''

class L(object):
    """
    Validates the length of a string.

    :param min:
        The minimum required length of the string. If not provided, minimum
        length will not be checked.
    :param max:
        The maximum length of the string. If not provided, maximum length
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)d` and `%(max)d` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """
    def __init__(self, min=-1, max=-1, message=None):
        assert min != -1 or max != -1, 'At least one of `min` or `max` must be specified.'
        assert max == -1 or min <= max, '`min` cannot be more than `max`.'
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = field.ngettext('Field must be at least %(min)d character long.',
                                             'Field must be at least %(min)d characters long.', self.min)
                elif self.min == -1:
                    message = field.ngettext('Field cannot be longer than %(max)d character.',
                                             'Field cannot be longer than %(max)d characters.', self.max)
                elif self.min == self.max:
                    message = field.ngettext('Field must be exactly %(max)d character long.',
                                             'Field must be exactly %(max)d characters long.', self.max)
                else:
                    message = field.gettext('Field must be between %(min)d and %(max)d characters long.')

            raise ValidationError(message % dict(min=self.min, max=self.max, length=l))


class AddUserForm(FlaskForm):
    login      = StringField('Login', validators=[InputRequired()],description="No debe existir, Obligatorio*")
    password   = PasswordField('Password', validators=[InputRequired(),EqualTo('confirm',message="Los Passwords deben ser iguales.")])
    confirm    = PasswordField('Confirmar Password')
    nombres    = StringField('Nombres', validators=[InputRequired()],description="Obligatorio*")
    apellidos  = StringField('Apellidos', validators=[InputRequired()],description="Obligatorio*")
    groups     = SelectField('Grupos',choices=list(map(lambda g: g.group,Groups.query.all())) + [""] )

    def validate_login(self,field):
        if (Users.query.filter_by(login = field.data).first() is not None):
            print(">:(")
            self.login.errors += (ValidationError("El usuario pertenece ya al sistema."),)
            raise ValidationError("El usuario pertenece ya al sistema.")

    def commit(self):
        login     = self.login.data
        password  = self.password.data
        nombres   = self.nombres.data
        apellidos = self.apellidos.data
        groups    = UserViewAPI.Parse.parseGroup(self.groups.data)
        u = Users(login=login,
            password=password,
            name=nombres,
            surname=apellidos,
            group_user=groups)
        UserControlAPI.Control.addUser(u)

    
class ModifyUserForm(FlaskForm):
    login      = StringField('Login', validators=[InputRequired()],description="No debe existir, Obligatorio*",render_kw={'readonly':'readonly'})
    name       = StringField('Nombres', validators=[InputRequired()],description="Obligatorio*")
    surname    = StringField('Apellidos', validators=[InputRequired()],description="Obligatorio*")
    group_user   = SelectField('Grupos',choices=Groups.query.all() + [""] )
    cosecha_user = SelectField('Cosechas',choices=Cosecha.query.all() + [""] )

    def commit(self,mode : str):
        login   = UserViewAPI.Parse.parseLogin(self.login.data)
        user    = UserControlAPI.Data.lookupUser(login)

        assert(user is not None)

        if mode == 'Eliminar':
            UserControlAPI.Control.deleteUser(user)
        else:
            assert(mode == 'Editar')
            login   = UserViewAPI.Parse.parseLogin(self.login.data)
            name    = UserViewAPI.Parse.parseName(self.name.data)
            surname = UserViewAPI.Parse.parseSurname(self.surname.data)
            group   = UserViewAPI.Parse.parseGroup(self.group_user.data)
            cosecha = UserViewAPI.Parse.parseDate(self.cosecha_user.data)

            setattr(user,'name',name)
            setattr(user,'surname',surname)
            setattr(user,'group_user',group)
            setattr(user,'cosecha_user',cosecha)
        
        ActiveApp.getDB().session.commit()

class AddCosechaForm(FlaskForm):
    ID         = IntegerField('ID', validators=[InputRequired(),NumberRange(min=0)],description="No debe existir, no negativo, Obligatorio*")
    description = StringField('Descripcion', validators=[InputRequired()])
    start_date  = DateField('Inicio', validators=[InputRequired()],description="Obligatorio* YYYY-MM-DD")
    end_date    = DateField('Cierre', validators=[InputRequired()],description="Obligatorio* YYYY-MM-DD")

    def commit(self):
        ID : int | None         = self.ID.data
        description : str        = self.description.data 
        start_date : date | None = self.start_date.data
        end_date   : date | None = self.end_date.data
        c = Cosecha(ID=ID,
            description=description,
            start_date=start_date,
            end_date=end_date,
            is_enabled=True)
        CosechaControlAPI.Control.addCosecha(c)

class ModifyCosechaForm(FlaskForm):
    ID         = IntegerField('ID', validators=[InputRequired(),NumberRange(min=0)],description="No debe existir, no negativo, Obligatorio*")
    description = StringField('Descripcion', validators=[InputRequired()])
    start_date  = DateField('Inicio', validators=[InputRequired()],description="Obligatorio* YYYY-MM-DD")
    end_date    = DateField('Cierre', validators=[InputRequired()],description="Obligatorio* YYYY-MM-DD")

    def commit(self,mode : str):
        ID : int | None         = self.ID.data
        cosecha  = CosechaControlAPI.Data.lookupCosecha(ID)

        assert(cosecha is not None)

        if mode == 'Eliminar':
            CosechaControlAPI.Control.deleteCosecha(cosecha)
        elif mode == 'Editar':
            description : str         = self.description.data 
            start_date  : date | None = self.start_date.data
            end_date    : date | None = self.end_date.data

            setattr(cosecha,'ID',ID)
            setattr(cosecha,'description',description)
            setattr(cosecha,'start_date',start_date)
            setattr(cosecha,'end_date',end_date)
        elif mode == "Pause":
            cosecha.is_enabled = not cosecha.is_enabled
        else:
            pass
            
        
        ActiveApp.getDB().session.commit()


def validate_CI(form, field):
    if(Persona.query.filter_by(CI = field.data).first() is not None):
        raise ValidationError("La CI ya esta en el sistema.")

    if re.search("[V,J,E](-\d)",field.data)==None:
        raise ValidationError("Formato erroneo de cedula, debe ser: V-22222.")
    
def validate_phone(form,field):
    if re.search("\d{4}(-\d{7})", field.data)==None:
        raise ValidationError("El numero no cumple el formado ddd-ddddddd.")

class AddProducerForm(FlaskForm):
    CI                  = StringField('Cedula', validators=[InputRequired(),validate_CI],description="No debe existir, Obligatorio*")
    surname             = StringField('Apellidos', validators=[InputRequired()])
    name                = StringField('Nombres', validators=[InputRequired()])
    localPhone          = StringField('Telefono local', validators=[InputRequired(),validate_phone])
    cellPhone           = StringField('Telefono celular', validators=[InputRequired(),validate_phone],description="Obligatorio*")
    persona_productor   = SelectField('Tipo de productor', choices=list(map(lambda tp: tp.description,TipoProductor.query.all())) )
    dir1                = StringField('Direccion 1', validators=[InputRequired()],description="Obligatorio*")
    dir2                = StringField('Direccion 2', validators=[InputRequired()],description="Obligatorio*")

def validate_Description(form, field):
    if (TipoProductor.query.filter_by(description = field.data).first() is not None):
        raise ValidationError("El usuario pertenece ya al sistema.")

class AddTypeOfProducer(FlaskForm):
    ID          = StringField('ID', validators=[InputRequired()],description="No debe existir, Obligatorio*")
    description = StringField('description', validators=[InputRequired(),validate_Description])
    precio      = StringField('precio', validators=[InputRequired()],description="No debe existir, Obligatorio*")

def validate_CI_Buy(form, field):
    if re.search("[V,J,E](-\d)",field.data)==None:
        raise ValidationError("Formato erroneo de cedula, debe ser: V-22222.")

def valid_ID_buy(form, field):
    if(Compra.query.filter_by(ID = field.data).first() is not None):
        raise ValidationError("El ID ya esta en el sistema.")

class AddBuy(FlaskForm): 
    ID             = IntegerField('ID', validators=[InputRequired(),NumberRange(min=0),valid_ID_buy],description="No debe existir, no negativo, Obligatorio*")
    date           = DateField('date', format='%Y-%m-%d', validators=[InputRequired()])
    CI             = StringField('CI', validators=[InputRequired(),validate_CI_Buy],description="No debe existir, Obligatorio*")
    precio         = IntegerField('precio', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")
    clase_cacao    = StringField('clase_cacao', validators=[InputRequired()],description="No debe existir, Obligatorio*")
    cantidad       = IntegerField('cantidad', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")
    humedadPer     = IntegerField('humedadPer', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")
    mermaPer       = IntegerField('mermaPer', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")
    observaciones  = StringField('observaciones', validators=[InputRequired()],description="No debe existir, Obligatorio*")
    recolector_ID  = IntegerField('recolector_ID', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")
    cosecha_ID     = IntegerField('cosecha_ID', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")
    form_type      = StringField('form_type', validators=[InputRequired()],description="No debe existir, no negativo, Obligatorio*")

