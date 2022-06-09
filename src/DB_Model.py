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


group_user = db.Table("group_user",
    db.Model.metadata,
    db.Column('login',db.Text,db.ForeignKey('users.login'),primary_key=True),
    db.Column('group',db.Text,db.ForeignKey('groups.group'),primary_key=True)
    )

cosecha_user = db.Table("cosecha_user",
    db.Model.metadata,
    db.Column('login',db.Text,db.ForeignKey('users.login'),primary_key=True),
    db.Column('cosecha',db.Text,db.ForeignKey('cosecha.start_date'),primary_key=True),
    db.Column('cosecha',db.Text,db.ForeignKey('cosecha.end_date'),primary_key=True)
    )

class Groups(db.Model):
    __tablename__ = "groups"
    group = db.Column(db.Text,primary_key=True)
    group_user = db.relationship("Users",secondary=group_user,lazy="subquery",back_populates="group_user")

    def __repr__(self) -> str:
        return f'<group: {self.group}>'


class Users(db.Model):
    __tablename__ = "users"
    login        = db.Column(db.Text,primary_key=True)
    name         = db.Column(db.Text,nullable=False)
    surname      = db.Column(db.Text,nullable=False)
    password     = db.Column(db.Text)
    group_user   = db.relationship("Groups",secondary=group_user,lazy="subquery",back_populates="group_user")
    cosecha_user = db.relationship("Cosecha",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")

    def __repr__(self) -> str:
        return f'<login: {self.login}\npassword: {self.password}\ngroup_user:{self.group_user}\ncosecha_user:{self.cosecha_user}>'


class Cosecha(db.Model):
    __tablename__ = "cosecha"
    start_date = db.Column(db.Date,primary_key=True)
    end_date   = db.Column(db.Date,primary_key=True)

    cosecha_user = db.relationship("Users",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")

    def __repr__(self) -> str:
        return f'<start_date: {str(self.start_date)}\nend_date: {str(self.end_date)}'



