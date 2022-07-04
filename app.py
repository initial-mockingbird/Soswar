from numpy import append
from sqlalchemy import column
from init import ActiveApp
ActiveApp.production()
from flask import  make_response, redirect, Blueprint, request

from flask import render_template,request, redirect
from src.PORM import AdminAPI, GroupControlAPI,UserControlAPI, loadFakeData
from src.DB_Model import Users, Encrypt, Groups, Cosecha, Persona, TipoProductor
from src.login import login
from src.accessControl import accessControl
from src.producers import data_producers, producers
from src.cosecha import cosecha
from src.compras import compras
from datetime import date 
from flask_wtf import FlaskForm

app = ActiveApp.getApp()
app.register_blueprint(login)
app.register_blueprint(accessControl)
app.register_blueprint(producers)
app.register_blueprint(cosecha)
app.register_blueprint(compras)

# Here we will save all the fake data for testing and develop 
#loadFakeData()

@app.route('/', methods=('GET', 'POST'))
def index():
    form     = FlaskForm()
    login    = request.cookies.get('login')
    user     = Users.query.filter_by(login=login).first()
    if (user is not None):
        return redirect('/control')
    return render_template('mainArea.html', htmlFile='login.html', cssFile=['css/main.css','css/login.css'],form=form)
    #return render_template('index.html',form=form)


if __name__=="__main__":
    app.run(debug=True)