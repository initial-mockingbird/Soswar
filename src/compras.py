from ast import Return
from xmlrpc.client import boolean
from flask import  url_for, make_response, redirect, Blueprint, request, abort
import flask
from numpy import product
from sqlalchemy import column
from src.DB_Model import Encrypt, Persona, Compra
from flask import render_template,request, redirect
from src.PORM import AdminAPI
from src.forms import *
from flask_wtf import FlaskForm
from src.validators import check_privileges
from src.PORM import CosechaControlAPI, CompraControlAPI
from datetime import date, MINYEAR, MAXYEAR, datetime

# Auxiliar functions
def getCosechaName( c:Cosecha ):
    meses  = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    cosechaName = ""
    cosechaName += meses[int(c.start_date.strftime("%m"))-1]
    cosechaName += " - "
    cosechaName += meses[int(c.end_date.strftime("%m"))-1]
    return cosechaName

compras= Blueprint('compras', __name__,template_folder='templates',static_folder='static')

# Routes for the interface with their respective initializations

# Add a 
@compras.route('/compras/<cosechaID>',methods=('GET', 'POST'))
def data_compras( cosechaID : int ):
    # We get the data of the current cosecha (in invalid case => 404)
    currentCosecha = CosechaControlAPI().Data().lookupCosecha( cosechaID )
    if currentCosecha==None: abort(404)
    cosechaName = getCosechaName( currentCosecha )

    # Name of each column in the grid
    fields = CompraControlAPI().Data().fieldsUI()
    # List with all the buys
    filterByID = request.args.get('filterByID', None)
    compras = currentCosecha.compras 
    if (filterByID is not None) and (filterByID!=""):
        compras = list(filter(lambda compra: str(compra.ID)==str(filterByID), compras) )
    for c in compras: c.addExtraAtt()

    # Variables for the Form (addUser)
    addCompraForm = AddBuy(request.form)
    addUserBool = request.args.get('AddCompra', None) 

    addCompraForm.form_type.default = "Crear"
    addCompraForm.cosecha_ID.default = cosechaID
    
    editID = request.args.get('editID', None)
    if editID is not None:
        compra = CompraControlAPI().Data().lookupCompra( editID ) 
        addCompraForm.ID.default = compra.ID
        addCompraForm.date.default = compra.date
        addCompraForm.CI.default = compra.CI
        addCompraForm.precio.default = compra.precio
        addCompraForm.clase_cacao.default = compra.clase_cacao
        addCompraForm.cantidad.default = compra.cantidad
        addCompraForm.humedadPer.default = compra.humedadPer
        addCompraForm.mermaPer.default = compra.mermaPer
        addCompraForm.observaciones.default = compra.observaciones
        addCompraForm.cosecha_ID.default = compra.cosecha_ID
        addCompraForm.recolector_ID.default = compra.recolector_ID
        addCompraForm.form_type.default = "Editar"
        addUserBool = True

    addCompraForm.process()

    return render_template(
        'mainArea.html', 
        htmlFile='compras.html', 
        cssFile=['css/producers.css', 'css/profiles.css', 'css/compras.css'], 
        cosechaName = cosechaName,
        cosechaID = cosechaID,
        # Table
        fields = fields,
        compras=compras,
        # Parameters for the FORM
        addCompraForm=addCompraForm,
        url='compras.compras_control',
        over = addUserBool,
        form = FlaskForm()
    )

# Routes in charge of the backend of the aplications

@compras.route('/comprasControl',methods=('GET', 'POST'))
def compras_control():
    # Boton de edicion
    if request.form['action'] == 'Editar':
        oldID = request.form['oldID']
        cosechaID=request.form['cosechaID']
        return redirect( url_for('compras.data_compras',cosechaID=cosechaID, editID=oldID ) )
    
    # Boron de eliminacion
    if request.form['action'] == 'Eliminar':
        ans = CompraControlAPI().Control().deleteCompra( request.form['oldID'] )
        flash("Eliminacion exitosa !!","greenMessage")
        return redirect('/compras/'+request.form['cosechaID'])
    
    # (en form) boton de cancelar
    cosechaID = request.form['cosecha_ID']
    if request.form['action'] == 'EXIT':
        return redirect('/compras/'+cosechaID)
    
    # (en form) editar o crear
    # Validamos al usuario
    form = AddBuy(request.form)
    valid : boolean = form.validate_on_submit()
    
    msg : str = ""
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            msg += err

    if valid or ( request.form['form_type']=='Editar' and msg=="El ID ya esta en el sistema." ):
        compraTemp = {}
        for field in CompraControlAPI().Data().pFields():
            if field=='date':
                compraTemp[field]= datetime.strptime(request.form[field], '%Y-%m-%d')
            else:
                compraTemp[field] = request.form[field]

        if request.form['form_type']=='Crear':
            ans = CompraControlAPI().Control().addCompra( Compra(**compraTemp) )
            flash( "Creacion exitosa!!", "greenMessage" )
        else:
            assert(request.form['form_type']=='Editar')
            ans = CompraControlAPI().Control().updateCompra( compraTemp )
            flash( "Edicion exitosa!!", "greenMessage" )
        return redirect('/compras/'+cosechaID)

    flash(msg,"redMessage")
    return redirect('/compras/'+cosechaID)

