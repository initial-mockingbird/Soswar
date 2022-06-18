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

"""
admin_user = Users(login="admin_user",password=Encrypt.encrypt("admin_user"),name="admin name",surname="admin surname")
dan   = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto")
angel = Users(login="angel",password=Encrypt.encrypt("angel"), name="Angel", surname="Garces")

admin = Groups(group="admin")
analist = Groups(group="analist")
cosecha1 = Cosecha(start_date=date(2022,3,1),end_date=date(2022,12,1))
cosecha2 = Cosecha(start_date=date(2022,6,1),end_date=date(2022,8,1))

admin_user.group_user.append(admin)
dan.group_user.append(analist)
dan.cosecha_user.append(cosecha1)
dan.cosecha_user.append(cosecha2)

# Personas -> TipoProductor
p1 = TipoProductor(description="productor1", ID=1)
p2 = TipoProductor(description="productor2", ID=2)
p3 = TipoProductor(description="productor3", ID=3)
p4 = TipoProductor(description="revendedor", ID=4)

pedro = Persona(name="Pedro", surname="Perez", CI="V-26175237", localPhone="0414256660", cellPhone="0414256660", dir1="los2K", dir2="1 transversal")
jose = Persona(name="Jose", surname="Jose", CI="V-26175238", localPhone="0414256660", cellPhone="0414256660", dir1="los2K", dir2="1 transversal")
tyron = Persona(name="Tyron", surname="Gonzales", CI="V-22175237", localPhone="0414256660", cellPhone="0414256660", dir1="los2K", dir2="1 transversal")
erwin = Persona(name="Erwin", surname="Schrödinger", CI="V-26172237", localPhone="0414256660", cellPhone="0414256660", dir1="los2K", dir2="1 transversal")

pedro.persona_productor.append(p1)
jose.persona_productor.append(p2)
tyron.persona_productor.append(p3)
erwin.persona_productor.append(p4)

ActiveApp.getDB().session.add(p1)
ActiveApp.getDB().session.add(p2)
ActiveApp.getDB().session.add(p3)
ActiveApp.getDB().session.add(p4)
ActiveApp.getDB().session.add(pedro)
ActiveApp.getDB().session.add(jose)
ActiveApp.getDB().session.add(tyron)
ActiveApp.getDB().session.add(erwin)
ActiveApp.getDB().session.add(admin_user)
ActiveApp.getDB().session.add(analist)
ActiveApp.getDB().session.add(cosecha1)
ActiveApp.getDB().session.add(cosecha2)
ActiveApp.getDB().session.add(dan)
ActiveApp.getDB().session.add(angel)
ActiveApp.getDB().session.commit()
"""

app = ActiveApp.getApp()
app.register_blueprint(login)
app.register_blueprint(accessControl)
app.register_blueprint(producers)

@app.route('/', methods=('GET', 'POST'))
def index():

    return make_response(redirect('/typeOfProducers'))
    columnName = [ 'Cedula:', 'Apellidos:', 'Nombres:', 'Telefono local:', 'Celular:', 'Tipo-productor:', 'Direccion 1:', 'Direccion 2:' ]
    columnId = AdminAPI.personaPublicFields()
    columnWidth = [ 120, 150, 150, 150, 150, 200, 200, 200 ]
    producersList = AdminAPI.getAllPersonas()
    typesOfProducers = AdminAPI.getAllTypeOfProducers()

    return render_template('mainArea.html', htmlFile='dataProductors.html', cssFile='css/producers.css', columnName=columnName, columnWidth=columnWidth, columnId=columnId, producersList=producersList, typesOfProducers=typesOfProducers)
    login    = request.cookies.get('login')
    user     = Users.query.filter_by(login=login).first()
    if (user is not None):
        return redirect('/control')
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)