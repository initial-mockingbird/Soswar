from ast import Return
from flask import  url_for, make_response, redirect, Blueprint, request
from numpy import product
from src.DB_Model import Encrypt, Persona
from flask import render_template,request, redirect
from src.PORM import AdminAPI
from src.forms import *
from flask_wtf import FlaskForm
from src.validators import check_privileges

producers= Blueprint('producers', __name__,template_folder='templates',static_folder='static')

# Routes for the interface with their respective initializations

@producers.route('/dataProducers',methods=('GET', 'POST'))
@check_privileges(['analist'])
def data_producers():
    # GET parameters
    filterByCI = request.args.get('filterByCI', None)
    filterByCI = None if filterByCI=="" else filterByCI

    redMessage:str= request.args.get('redMessage', None)
    #redMessage = "" if redMessage==None else redMessage

    greenMessage:str= request.args.get('greenMessage', None)
    #greenMessage = "" if greenMessage==None else greenMessage

    # Name of each column in the grid
    columnName = [ 'Cedula:', 'Apellidos:', 'Nombres:', 'Telefono local:', 'Celular:', 'Tipo-recolector:', 'Direccion 1:', 'Direccion 2:' ]
    # Internal id number columns for the backend
    columnId = AdminAPI.personaPublicFields()
    # Width of each columns in the grid
    columnWidth = [ 120, 150, 150, 150, 150, 200, 200, 200 ]
    # Rows in the grid ( each one will be a FORM )
    producersList = AdminAPI.getAllPersonas( filterByCI ) 
    # => Sppecial field in the grid ( the options in the column 5 )
    typesOfProducers = AdminAPI.getAllTypeOfProducers()

    # Variables for the Form (addUser)
    addUserForm = AddProducerForm(request.form)
    addUserBool = request.args.get('addProductor', None)

    flash(redMessage,'redMessage')
    flash(greenMessage,'greenMessage')
    return render_template(
        'mainArea.html', 
        htmlFile='dataProductors.html', 
        cssFile=['css/producers.css', 'css/profiles.css'], 
        columnName=columnName, 
        columnWidth=columnWidth, 
        columnId=columnId, 
        producersList=producersList, 
        typesOfProducers=typesOfProducers, 
        #redMessage=redMessage, 
        #greenMessage=greenMessage,
        # Parameters for the FORM
        addUserForm=addUserForm,
        url='producers.addProducers',
        over = addUserBool,
        form = FlaskForm()
    )

@producers.route('/typeOfProducers',methods=('GET', 'POST'))
@check_privileges(['analist'])
def type_of_data_producers():
    filterByDescription = request.args.get('filterByDescription', None)
    filterByDescription = None if filterByDescription=="" else filterByDescription

    redMessage:str= request.args.get('redMessage', None)
    #redMessage = "" if redMessage==None else redMessage

    greenMessage:str= request.args.get('greenMessage', None)
    #greenMessage = "" if greenMessage==None else greenMessage
    
    # Name of each column in the grid
    columnName = [ 'ID:', 'Descripcion:', 'precio' ]
    # Internal id number columns for the backend
    columnId = AdminAPI.typeOfProducerPublicFields()
    # Width of each columns in the grid
    columnWidth = [ 50, 200, 50 ]
    # Rows in the grid ( each one will be a FORM )
    typesOfProducers = AdminAPI.getAllTypeOfProducers( filterByDescription )

    # Variables for the Form (addUser)
    addUserForm = AddTypeOfProducer(request.form)
    addUserBool = request.args.get('addProductor', None)

    flash(redMessage,'redMessage')
    flash(greenMessage,'greenMessage')
    return render_template(
        'mainArea.html', 
        htmlFile='producers.html', 
        cssFile=['css/main.css','css/producers.css', 'css/profiles.css'], 
        columnName=columnName, 
        columnWidth=columnWidth, 
        columnId=columnId, 
        typesOfProducers=typesOfProducers, 
        #redMessage=redMessage, 
        #greenMessage=greenMessage,
        # Parameters for the FORM
        addUserForm=addUserForm,
        url='producers.addTypeOfProducer',
        over = addUserBool,
        form = FlaskForm()
    )

# Routes in charge of the backend of the aplications

@producers.route('/updateProducers',methods=('GET', 'POST'))
def process_data_producers():
    if request.method != 'POST':
        return

    if request.form['action'] == 'Editar':
        # Validamos al usuario
        form = AddProducerForm(request.form)
        if form.validate_on_submit():
            AdminAPI.updPerson( request.form['oldCI'], request.form )  
            return redirect( url_for('producers.data_producers', greenMessage="Edicion hecha con exito !!") ) 
        else:
            msg : str = ""
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    if msg=="":
                        msg += err

            return redirect( url_for('producers.data_producers', redMessage=msg) ) 
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

# Add routes

@producers.route('/addProducers',  methods=('GET','POST'))
def addProducers():
    if request.form['action'] == 'EXIT':
        return redirect(url_for('producers.data_producers'))
    
    # Validamos al usuario
    form = AddProducerForm(request.form)
    if form.validate_on_submit():
        AdminAPI.addPerson( request.form )
        return redirect(url_for('producers.data_producers', greenMessage="Productor agregado con exito !!")) 

    msg : str = ""
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            if msg=="":
                msg += err

    return redirect( url_for('producers.data_producers', redMessage=msg) )

@producers.route('/addTypeOfProducer',  methods=('GET','POST'))
def addTypeOfProducer():
    if request.form['action'] == 'EXIT':
        return redirect(url_for('producers.type_of_data_producers'))
    
    form = AddTypeOfProducer(request.form)
    if form.validate_on_submit():
        AdminAPI.addTypeOfProducer( request.form, [] )
        return redirect(url_for('producers.type_of_data_producers', greenMessage="Tipo de productor agregado con exito !!"))

    msg : str = ""
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            if msg=="":
                msg += err
    return redirect( url_for('producers.type_of_data_producers', redMessage=msg) )


