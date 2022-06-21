
from typing import List
from flask import redirect, render_template, Blueprint, request, url_for
from init import ActiveApp
from src.DB_Model import Encrypt, Users, Groups, group_user
from src.validators import check_privileges
from src.PORM import AdminAPI
from src.forms import *

accessControl= Blueprint('accessControl', __name__,template_folder='templates',static_folder='static')


@accessControl.route('/addUser',  methods=('GET','POST'))
@check_privileges(['admin'])
def addUser():
    print("ENTRANDO ACA")
    
    print(request.form)
    if request.form['action'] == 'EXIT':
        redirect(url_for('accessControl.access_control'))
    
    form = AddUserForm(request.form)
    if form.validate_on_submit():
        print("AAAAAAAAAAAAAAAAAAA")
        print(request.form)
        if request.form['action'] != 'EXIT':
            login     = form.login.data
            password  = form.password.data
            nombres   = form.nombres.data
            apellidos = form.apellidos.data
            groups    = ModifyUserFormParser.parseGroup(form.groups.data)
            user = Users(login=login,
                password=password,
                name=nombres,
                surname=apellidos,
                group_user=groups)
            ActiveApp.getDB().session.add(user)
        ActiveApp.getDB().session.commit()


    return redirect(url_for('accessControl.access_control'))



@accessControl.route('/modifyUser',  methods=('GET','POST'))
@check_privileges(['admin'])
def modifyUser():
    form = ModifyUserForm(request.form)
    if form.validate_on_submit():
        login   = ModifyUserFormParser.parseLogin(form.login.data)
        user = Users.query.filter_by(login=login)
        print(request.form)
        if request.form['action'] == 'Eliminar':
            print("En eliminar")
            user.delete()
        else:
            print("En editar")
            assert(request.form['action'] == 'Editar')
            login   = ModifyUserFormParser.parseLogin(form.login.data)
            name    = ModifyUserFormParser.parseName(form.name.data)
            surname = ModifyUserFormParser.parseSurname(form.surname.data)
            group   = ModifyUserFormParser.parseGroup(form.group_user.data)
            cosecha = ModifyUserFormParser.parseDate(form.cosecha_user.data)

            user = user.first()
            setattr(user,'name',name)
            setattr(user,'surname',surname)
            setattr(user,'group_user',group)
            setattr(user,'cosecha_user',cosecha)
        ActiveApp.getDB().session.commit()


    return redirect(url_for('accessControl.access_control'))


def mkForm(pfields,pInfo,form):
    for field in pfields:
        properties = {}
        containerAttrs = {}
        if (not pfields[field]['modifiable']):
            properties['readonly '] = 'readonly'
        if (pfields[field]['valueType'] == str):
            properties['value'] = pInfo[field]
            properties['class'] = 'stringBox'
        else:
            properties['class'] = 'defaultBox'
            aux = pInfo[field][0] if pInfo[field] != [] else "" 
            setattr(getattr(form,field),'default',aux)
        
        setattr(getattr(form,field),'render_kw',properties)
        setattr(getattr(form,field),'containerAttrs',containerAttrs)
    form.process()

        

@accessControl.route('/control',  methods=('GET', 'POST'))
@check_privileges(['admin'])
def access_control():
    Node = request.args.get('action', None)
    coupled             = AdminAPI.userPublicInfo()
    fields              = AdminAPI.pFields()
    forms = []
    for c in coupled:
        form = ModifyUserForm(request.form)
        mkForm(fields,c,form)
        forms.append(form)

    fs = []
    for form in forms:
        aux = []
        for field in fields:
            aux.append(getattr(form,field))
        fs.append(aux)

    addUserForm = AddUserForm(request.form)
    return render_template('accessControl.html',
        forms=zip(fs,forms),
        fields=fields,
        over=Node,
        addUserForm=addUserForm,
        url='accessControl.addUser')

