
from typing import List
from flask import render_template, Blueprint
from requests import request
from init import ActiveApp
from src.DB_Model import Encrypt, Users, Groups, group_user
from src.validators import check_privileges
from src.PORM import AdminAPI

accessControl= Blueprint('accessControl', __name__,template_folder='templates',static_folder='static')

@accessControl.route('/control',  methods=('GET', 'POST'))
@check_privileges(['admin'])
def access_control():
    coupled             = AdminAPI.userPublicInfo()
    fields              = AdminAPI.userPublicFields()
    print(f"\n\n\nCOUPLED:{coupled}\n\n\n")
    print(f"\n\n\nFIELDS:{fields.keys()}\n\n\n")
    return render_template('accessControl.html',coupled=coupled, fields = fields.keys(), selected=None)


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