
from typing import List
from flask import redirect, render_template, Blueprint, request, url_for
from init import ActiveApp
from src.DB_Model import Encrypt, Users, Groups, group_user
from src.validators import check_privileges
from src.PORM import AdminAPI
from src.forms import *

accessControl= Blueprint('accessControl', __name__,template_folder='templates',static_folder='static')

def classChooser(c,d):
    match c:
        case str:
            d['class'] = 'stringBox'


def mkForm(pfields,pInfo,form):
    for field in pfields:
        properties = {}
        properties['value'] = pInfo[field]
        containerAttrs = {}
        classChooser(pfields[field]['valueType'],containerAttrs)
        if (not pfields[field]['modifiable']):
            properties['disabled'] = 'disabled'
        if (pfields[field]['valueType'] == str):
            properties['class'] = 'stringBox'
        else:
            properties['class'] = 'defaultBox'
        setattr(getattr(form,field),'render_kw',properties)
        setattr(getattr(form,field),'containerAttrs',containerAttrs)
        

@accessControl.route('/control',  methods=('GET', 'POST'))
@check_privileges(['admin'])
def access_control():
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

    return render_template('accessControl.html',forms=fs,fields=fields)



def createUser(form):
    print(f"\n\n\nFORMCITO:{form}\n\n\n")

@accessControl.route('/addUser',  methods=('GET', 'POST'))
@check_privileges(['admin'])
def add_user():
    print(f"\n\n\nGRUPITOS:{Groups.query.all()}\n\n\n")
    form = AddUserForm(request.form)

    if (request.method == 'POST'):

        if (request.form['submit'] == 'CLEAN'):
            return redirect(url_for('accessControl.add_user'))

        if(form.validate()):
            createUser(form)
            return redirect(url_for('accessControl.access_control'))
        else:
            return redirect(url_for('accessControl.add_user'))
    return render_template('addUserT.html',form=form)

@accessControl.route('/update',  methods=('GET', 'POST'))
def addRandomUsers():
    
    newAdmin = Users(login="newAdim",password=Encrypt.encrypt("newAdim"),name="newAdim name",surname="newAdim surname")
    jean   = Users(login="jean",password=Encrypt.encrypt("jean"), name="jean", surname="gonzales")

    contaduria = Groups(group="contaduria")
    
    adminGroup = AdminAPI.lookupGroup('admin')
    assert(adminGroup is not None)
    AdminAPI.addGroup(contaduria)
    AdminAPI.addUser(jean)
    AdminAPI.addUser(newAdmin)
    AdminAPI.addGroupToUser(adminGroup,newAdmin)
    AdminAPI.addGroupToUser(contaduria,jean)
    AdminAPI.deleteUser('dan')

    return f"<h1>DONE</h1>"