
from flask import render_template,request, redirect
from init import app
from src.DB_Model import Users, db, Encrypt, Groups, Cosecha
from src.login import login
from src.accessControl import accessControl
from datetime import date 


db.create_all()

'''
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

db.session.add(admin_user)
db.session.add(analist)
db.session.add(cosecha1)
db.session.add(cosecha2)
db.session.add(dan)
db.session.add(angel)
db.session.commit()
'''


app.register_blueprint(login)
app.register_blueprint(accessControl)

@app.route('/', methods=('GET', 'POST'))
def index():
    login    = request.cookies.get('login')
    user     = Users.query.filter_by(login=login).first()
    if (user is not None):
        return redirect('/control')
    return render_template('index.html')









if __name__=="__main__":
    app.run(debug=True)