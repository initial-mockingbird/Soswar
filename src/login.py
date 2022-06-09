from flask import  make_response, redirect, Blueprint, request
from src.DB_Model import Encrypt

login= Blueprint('login', __name__,template_folder='templates',static_folder='static')


@login.route('/login',methods=('GET', 'POST'))
def process_login():
    if request.method != 'POST':
        return
    login    : str = request.form['login']
    password : str = Encrypt.encrypt(request.form['password'])
    resp = make_response(redirect('/control'))
    resp.set_cookie('login', login)
    resp.set_cookie('password', password)
    
    return resp