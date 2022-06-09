from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
import hashlib
from init import app

class Encrypt():
    @staticmethod
    def encrypt(s : str) -> str:
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

db  = SQLAlchemy(app)

"""
class Group(db.Model):
    __tablename__ = "group"
    group = db.Column(db.Text,primary_key=True)
    users = relationship("User",secondary="group_user")

    def __repr__(self) -> str:
        return f'<group: {self.group}>'
"""

class User(db.Model):
    __tablename__ = "user"
    login    = db.Column(db.Text,primary_key=True)
    password = db.Column(db.Text)
    #groups   = relationship("Group",secondary="group_user")
    #cosechas = relationship("Cosecha",secondary="cosecha_user")

    def __repr__(self) -> str:
        return f'<login: {self.login}\tpassword: {self.password}>\n'

"""
class Cosecha(db.Model):
    __tablename__ = "cosecha"
    start_date = db.Column(db.Date,primary_key=True)
    end_date   = db.Column(db.Date,primary_key=True)

    users = relationship("User",secondary="cosecha_user")

    def __repr__(self) -> str:
        return f'<start_date: {str(self.start_date)}\nend_date: {str(self.end_date)}'


class GroupUserRel(db.Model):
    __tablename__ = "group_user"
    login    = db.Column(db.Text, db.ForeignKey('user.login'), primary_key=True, autoincrement=False)
    password = db.Column(db.Text, db.ForeignKey('user.password'), primary_key=True, autoincrement=False)
    group    = db.Column(db.Text, db.ForeignKey('group.group'), primary_key=True, autoincrement=False)

    user_rel  = relationship(User ,backref=backref("group_user", cascade="all, delete-orphan"))
    group_rel = relationship(Group,backref=backref("group_user", cascade="all, delete-orphan"))


class CosechaUserRel(db.Model):
    __tablename__ = "cosecha_user"
    login    = db.Column(db.Text, db.ForeignKey('user.login'), primary_key=True, autoincrement=False)
    password = db.Column(db.Text, db.ForeignKey('user.password'), primary_key=True, autoincrement=False)
    start_date = db.Column(db.Date, db.ForeignKey('cosecha.start_date'), primary_key=True)
    end_date = db.Column(db.Date, db.ForeignKey('cosecha.end_date'), primary_key=True)

    suser_rel    = relationship(User ,backref=backref("cosecha_user", cascade="all, delete-orphan"))
    cosecha_rel = relationship(Cosecha,backref=backref("cosecha_user", cascade="all, delete-orphan"))

"""
