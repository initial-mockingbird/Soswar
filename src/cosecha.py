
from faulthandler import is_enabled
from typing import Any, List
from flask import redirect, render_template, Blueprint, request, url_for, Request
from init import ActiveApp
from src.validators import check_privileges
from src.PORM import CosechaViewAPI, UserControlAPI, mkForm
from src.forms import AddCosechaForm, ModifyCosechaForm
cosecha= Blueprint('cosecha', __name__,template_folder='templates',static_folder='static')


@cosecha.route('/addCosecha',  methods=('GET','POST'))
@check_privileges(['admin'])
def addCosecha():
    if request.form['action'] == 'EXIT':
        return redirect(url_for('cosecha.cosechaControl'))
    form = AddCosechaForm(request.form)
    if form.validate_on_submit():
        form.commit()

    return redirect(url_for('cosecha.cosechaControl'))


@cosecha.route('/modifyCosecha',  methods=('GET','POST'))
@check_privileges(['admin','analist'])
def modifyCosecha():
    form = ModifyCosechaForm(request.form)

    if('redirect' in request.form ):
        return redirect(url_for('compras.data_compras',cosechaID=form.ID.data))

    if('download' in request.form):
        return redirect(url_for('compras.compras_pdf',cosechaID=form.ID.data,fields={}))
    
    if('listar' in request.form):
        return redirect(url_for('compras.data_lista_compras',cosechaID=form.ID.data,fields={}))
    

    if form.validate_on_submit():
        form.commit(request.form['action'])

    return redirect(url_for('cosecha.cosechaControl'))
    return redirect(url_for('compras.cosechaControl'))


def buildPageArgs(request : Request):
    return {
        'AddCosecha':request.args.get('AddCosecha', None),
        'SearchCosecha':request.args.get('SearchCosecha', None),
        'FilterByID':request.args.get('FilterByID', None)
    }
    

@cosecha.route('/cosechas',  methods=('GET', 'POST'))
@check_privileges(['admin', 'analist'])
def cosechaControl():
    args                = buildPageArgs(request)
    Node                = args['AddCosecha']
    coupled             = CosechaViewAPI.cosechaPublicInfo()
    fields              = CosechaViewAPI.pFields()
    fields.pop('is_enabled')
    args                = buildPageArgs(request)
    forms = []
    enabled = []
    for c in coupled:
        print(c)
        form = ModifyCosechaForm(request.form)
        if args['SearchCosecha'] is not None and args['FilterByID'] is not None and args['FilterByID'] != "":
            aux = args['FilterByID'] 
            try:
                n = int(aux)
                if(c['ID'] != n):
                    continue
            except:
                pass 
        is_enabled = c['is_enabled']
        enabled.append(is_enabled)
        if not is_enabled:
            _fields = {}
            for k in fields:
                _fields[k] = fields[k]
                _fields[k]['modifiable']=False
            fields = _fields
        
        c.pop('is_enabled')
        mkForm(fields,c,form)
        forms.append(form)


    fs = []
    for form in forms:
        aux = []
        for field in fields:
            aux.append(getattr(form,field))
        fs.append(aux)

    addCosechaForm = AddCosechaForm(request.form)
    zs = list(zip(fs,forms,enabled))

    login    = request.cookies.get('login')
    user = UserControlAPI.Data.lookupUser(login)
    assert (user is not None)
    b = any([g.group in ["admin"] for g in user.group_user])

    return render_template('cosechasT.html',
        forms=zs,
        fields=fields,
        over=Node,
        addCosechaForm=addCosechaForm,
        isAdmin = b,
        url='cosecha.addCosecha')

