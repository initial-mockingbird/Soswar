
from typing import Any, List
from flask import redirect, render_template, Blueprint, request, url_for
from init import ActiveApp
from src.DB_Model import Encrypt, Users, Groups, group_user
from src.validators import check_privileges
from src.PORM import UserControlAPI, UserViewAPI, mkForm
from src.forms import *

accessControl= Blueprint('accessControl', __name__,template_folder='templates',static_folder='static')


@accessControl.route('/addUser',  methods=('GET','POST'))
@check_privileges(['admin'])
def addUser():
    if request.form['action'] == 'EXIT':
        print("ACA")
        return redirect(url_for('accessControl.access_control'))
    form = AddUserForm(request.form)
    if form.validate_on_submit():
        form.commit()

    return redirect(url_for('accessControl.access_control'))


@accessControl.route('/modifyUser',  methods=('GET','POST'))
@check_privileges(['admin'])
def modifyUser():
    form = ModifyUserForm(request.form)
    if form.validate_on_submit():
        form.commit(request.form['action'])

    return redirect(url_for('accessControl.access_control'))


@accessControl.route('/control',  methods=('GET', 'POST'))
@check_privileges(['admin'])
def access_control():
    Node = request.args.get('action', None)
    coupled             = UserViewAPI.userPublicInfo()
    fields              = UserViewAPI.pFields()
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

