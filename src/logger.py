
from faulthandler import is_enabled
from typing import Any, List
from flask import redirect, render_template, Blueprint, request, url_for, Request
from init import ActiveApp
from src.validators import check_privileges
from src.PORM import CosechaViewAPI, LoggerControlAPI, LoggerViewAPI, UserControlAPI, mkForm
from src.forms import AddCosechaForm, LoggerForm, ModifyCosechaForm

logger= Blueprint('logger', __name__,template_folder='templates',static_folder='static')



@logger.route('/loggerDetails',  methods=('GET','POST'))
@check_privileges(['admin','analist'])
def loggerDetails():

    if request.form['action'] == 'EXIT':
        print("ACA")
        return redirect(url_for('logger.loggerControl'))

    form = LoggerForm(request.form)
    if('Detalles' in request.form ):
        redirect(url_for('logger.loggerControl',details=ID))

    if('Eliminar' in request.form):
        LoggerControlAPI.Control.deleteLog(ID)

    return redirect(url_for('logger.loggerControl'))


def buildPageArgs(request : Request):
    return {
        'Detalles':request.args.get('Detalles', None),
        'SearchCosecha':request.args.get('SearchCosecha', None),
        'FilterByID':request.args.get('FilterByID', None)
    }
    

@logger.route('/logs',  methods=('GET', 'POST'))
@check_privileges(['admin', 'analist'])
def loggerControl():
    args                = buildPageArgs(request)
    Node                = args['Detalles']
    coupled             = LoggerViewAPI.loggerPublicInfo() 
    fields              = LoggerViewAPI.pFields()
    args                = buildPageArgs(request)
    forms = []
    for c in coupled:
        form = LoggerForm(request.form)
        if args['SearchCosecha'] is not None and args['FilterByID'] is not None and args['FilterByID'] != "":
            aux = args['FilterByID'] 
            try:
                n = int(aux)
                if(c['ID'] != n):
                    continue
            except:
                pass 
        mkForm(fields,c,form)
        form.fill_defaults(c['ID'])
        print("=========================================")
        print(c)
        print(form.ID.data)
        print("=========================================")
        forms.append(form)

    fs = []
    for form in forms:
        aux = []
        for field in fields:
            aux.append(getattr(form,field))
        fs.append(aux)


    loggerDetailsForm = None
    if (Node is not None):
        print("-------------------------------")
        print("NOT NONEEEEEEEE")
        print(Node)
        print("-------------------------------")
        log : Logger = LoggerControlAPI.Data.lookupLog(Node)
        #loggerDetailsForm.fill(int(Node))
        loggerDetailsForm = LoggerForm(
            request.form,
            ID=str(log.ID),
            evento=log.evento,
            modulo=log.modulo,
            date=log.date,
            time=log.time,
            description=log.description,
            user_login=log.user_login
            )
        
    zs = list(zip(fs,forms))


    return render_template('loggerT.html',
        forms=zs,
        fields=fields,
        over=Node,
        loggerDetailsForm=loggerDetailsForm,
        url='logger.loggerDetails')

