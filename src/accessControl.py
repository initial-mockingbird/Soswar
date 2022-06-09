
from typing import List
from flask import render_template, Blueprint
from requests import request
from init import app
from src.DB_Model import Encrypt, Users, db, Groups, group_user
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