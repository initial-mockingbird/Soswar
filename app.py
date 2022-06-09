
from unittest import result
from flask import Flask, render_template
from flask import (request, redirect, session)
from sqlalchemy import true
from init import app
from src.DB_Model import Encrypt, User, db

db.create_all()

#admin = User(login="admin",password=Encrypt.encrypt("admin"))
#dan   = User(login="dan",password=Encrypt.encrypt("dan"))
#angel = User(login="angel",password=Encrypt.encrypt("angel"))

#db.session.add(admin)
#db.session.add(dan)
#db.session.add(angel)
#db.session.commit()

# print( User.query.all() ) 

# Ruta que se encarga de redireccionar al usuario al llenar el form
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        # Obtenemos los strings ingresados por el usuario
        username = request.form.get('login') 
        password = request.form.get('password') 

        # Hacemos una consulta a la BD para saber si el usuario existe
        result = User.query.filter_by(
            login = username,
            password=Encrypt.encrypt(password)
        ).first();

        # Si existe lo redirigimos a la pagina principal
        if result!=None:
            return render_template('mainT.html')
        else:
            return "<h1>Wrong username or password </h1>" 

    return render_template("index.html")

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)