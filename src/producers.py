from ast import Return
from flask import  url_for, make_response, redirect, Blueprint, request
from numpy import product
from src.DB_Model import Encrypt, Persona
from flask import render_template,request, redirect
from src.PORM import AdminAPI

producers= Blueprint('producers', __name__,template_folder='templates',static_folder='static')

# Routes for the interface with their respective initializations

@producers.route('/dataProducers',methods=('GET', 'POST'))
def data_producers():
    # GET parameters
    filterByCI = request.args.get('filterByCI', None)
    filterByCI = None if filterByCI=="" else filterByCI

    redMessage:str= request.args.get('redMessage', None)
    redMessage = "" if redMessage==None else redMessage

    greenMessage:str= request.args.get('greenMessage', None)
    greenMessage = "" if greenMessage==None else greenMessage

    # Name of each column in the grid
    columnName = [ 'Cedula:', 'Apellidos:', 'Nombres:', 'Telefono local:', 'Celular:', 'Tipo-productor:', 'Direccion 1:', 'Direccion 2:' ]
    # Internal id number columns for the backend
    columnId = AdminAPI.personaPublicFields()
    # Width of each columns in the grid
    columnWidth = [ 120, 150, 150, 150, 150, 200, 200, 200 ]
    # Rows in the grid ( each one will be a FORM )
    producersList = AdminAPI.getAllPersonas( filterByCI ) 
    # => Sppecial field in the grid ( the options in the column 5 )
    typesOfProducers = AdminAPI.getAllTypeOfProducers()

    return render_template('mainArea.html', htmlFile='dataProductors.html', cssFile='css/producers.css', columnName=columnName, columnWidth=columnWidth, columnId=columnId, producersList=producersList, typesOfProducers=typesOfProducers, redMessage=redMessage, greenMessage=greenMessage)

@producers.route('/typeOfProducers',methods=('GET', 'POST'))
def type_of_data_producers():
    filterByDescription = request.args.get('filterByDescription', None)
    filterByDescription = None if filterByDescription=="" else filterByDescription

    redMessage:str= request.args.get('redMessage', None)
    redMessage = "" if redMessage==None else redMessage

    greenMessage:str= request.args.get('greenMessage', None)
    greenMessage = "" if greenMessage==None else greenMessage
    
    # Name of each column in the grid
    columnName = [ 'ID:', 'Descripcion:' ]
    # Internal id number columns for the backend
    columnId = AdminAPI.typeOfProducerPublicFields()
    # Width of each columns in the grid
    columnWidth = [ 50, 200 ]
    # Rows in the grid ( each one will be a FORM )
    typesOfProducers = AdminAPI.getAllTypeOfProducers( filterByDescription )

    return render_template('mainArea.html', htmlFile='producers.html', cssFile='css/producers.css', columnName=columnName, columnWidth=columnWidth, columnId=columnId, typesOfProducers=typesOfProducers, redMessage=redMessage, greenMessage=greenMessage)

# Routes in charge of the backend of the aplications

@producers.route('/updateProducers',methods=('GET', 'POST'))
def process_data_producers():
    if request.method != 'POST':
        return
    
    if request.form['action'] == 'Editar':
        AdminAPI.updPerson( request.form['oldCI'], request.form )
        return redirect( url_for('producers.data_producers', greenMessage="Edicion hecha con exito !!") )
    else:
        AdminAPI.deletePersona( request.form['oldCI'] )
        return redirect( url_for('producers.data_producers', greenMessage="Eliminacion hecha con exito !!") )

@producers.route('/updateTypeOfProducer',methods=('GET', 'POST'))
def process_type_of_producers():
    if request.method != 'POST':
        return
    
    if request.form['action'] == 'Editar':
        AdminAPI.updTypeOfProducer( request.form['oldDescription'], request.form )
        return redirect( url_for('producers.type_of_data_producers', greenMessage="Edicion hecha con exito !!") ) 
    else:
        AdminAPI.deleteTypeOfProducer( request.form['oldDescription'] )
        return redirect( url_for('producers.type_of_data_producers', greenMessage="Eliminacion hecha con exito !!") ) 


