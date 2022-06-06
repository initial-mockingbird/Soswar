
from flask import Flask, render_template
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


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)