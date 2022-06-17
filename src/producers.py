from ast import Return
from flask import  make_response, redirect, Blueprint, request
from numpy import product
from src.DB_Model import Encrypt, Persona
from flask import render_template,request, redirect
from src.PORM import AdminAPI

producers= Blueprint('producers', __name__,template_folder='templates',static_folder='static')

@producers.route('/dataProducers',methods=('GET', 'POST'))
def data_producers():
    columnName = [ 'Cedula:', 'Apellidos:', 'Nombres:', 'Telefono local:', 'Celular:', 'Tipo-productor:', 'Direccion 1:', 'Direccion 2:' ]
    columnId = AdminAPI.personaPublicFields()
    columnWidth = [ 120, 150, 150, 150, 150, 200, 200, 200 ]
    producersList = AdminAPI.getAllPersonas()
    typesOfProducers = AdminAPI.getAllTypeOfProducers()

    return render_template('mainArea.html', htmlFile='dataProductors.html', cssFile='css/producers.css', columnName=columnName, columnWidth=columnWidth, columnId=columnId, producersList=producersList, typesOfProducers=typesOfProducers)

@producers.route('/typeOfProducers',methods=('GET', 'POST'))
def type_of_data_producers():
    columnName = [ 'ID:', 'Descripcion:' ]
    columnId = AdminAPI.typeOfProducerPublicFields()
    columnWidth = [ 50, 200 ]
    typesOfProducers = AdminAPI.getAllTypeOfProducers()

    return render_template('mainArea.html', htmlFile='producers.html', cssFile='css/producers.css', columnName=columnName, columnWidth=columnWidth, columnId=columnId, typesOfProducers=typesOfProducers)


@producers.route('/producers',methods=('GET', 'POST'))
def process_producers():
    if request.method != 'POST':
        return
    
    if request.form['action'] == 'Editar':
        AdminAPI.updPerson( request.form['oldCI'], request.form )
    else:
        AdminAPI.deletePersona( request.form['oldCI'] )

    return make_response(redirect('/dataProducers'))