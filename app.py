from numpy import append
from sqlalchemy import column
from init import ActiveApp
ActiveApp.production()
from flask import  make_response, redirect, Blueprint, request

from flask import render_template,request, redirect
from src.PORM import AdminAPI
from src.DB_Model import Users, Encrypt, Groups, Cosecha, Persona, TipoProductor
from src.login import login
from src.accessControl import accessControl
from src.producers import data_producers, producers
from datetime import date 
from flask_wtf import FlaskForm


app = ActiveApp.getApp()
app.register_blueprint(login)
app.register_blueprint(accessControl)
app.register_blueprint(producers)

@app.route('/', methods=('GET', 'POST'))
def index():

    #return make_response(redirect('/dataProducers'))
    '''
    columnName = [ 'Cedula:', 'Apellidos:', 'Nombres:', 'Telefono local:', 'Celular:', 'Tipo-productor:', 'Direccion 1:', 'Direccion 2:' ]
    columnId = AdminAPI.personaPublicFields()
    columnWidth = [ 120, 150, 150, 150, 150, 200, 200, 200 ]
    producersList = AdminAPI.getAllPersonas()
    typesOfProducers = AdminAPI.getAllTypeOfProducers()

    return render_template('mainArea.html', htmlFile='dataProductors.html', cssFile='css/producers.css', columnName=columnName, columnWidth=columnWidth, columnId=columnId, producersList=producersList, typesOfProducers=typesOfProducers)
    '''
    form     = FlaskForm()
    login    = request.cookies.get('login')
    user     = Users.query.filter_by(login=login).first()
    if (user is not None):
        return redirect('/control')
    return render_template('index.html',form=form)


if __name__=="__main__":
    app.run(debug=True)