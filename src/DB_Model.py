from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
import hashlib
from typing import Any
from init import ActiveApp

class Encrypt():
    @staticmethod
    def encrypt(s : str) -> str:
        return hashlib.sha256(s.encode('utf-8')).hexdigest()


group_user = ActiveApp.getDB().Table("group_user",
    ActiveApp.getDB().Model.metadata,
    ActiveApp.getDB().Column('login',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('users.login'),primary_key=True),
    ActiveApp.getDB().Column('group',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('groups.group'),primary_key=True)
    )


cosecha_user = ActiveApp.getDB().Table("cosecha_user",
    ActiveApp.getDB().Model.metadata,
    ActiveApp.getDB().Column('login',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('users.login'),primary_key=True),
    ActiveApp.getDB().Column('cosecha',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('cosecha.start_date'),primary_key=True),
    ActiveApp.getDB().Column('cosecha',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('cosecha.end_date'),primary_key=True)
    )

productor = ActiveApp.getDB().Table("productor",
    ActiveApp.getDB().Model.metadata,
    ActiveApp.getDB().Column('CI',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('persona.CI'),primary_key=True),
    ActiveApp.getDB().Column('description',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('tipo_productor.description'),primary_key=True)
    )

class Groups(ActiveApp.getDB().Model):
    __tablename__ = "groups"
    group = ActiveApp.getDB().Column(ActiveApp.getDB().Text,primary_key=True)
    group_user = ActiveApp.getDB().relationship("Users",secondary=group_user,lazy="subquery",back_populates="group_user")

    def __repr__(self) -> str:
        return f'{self.group}'


class Users(ActiveApp.getDB().Model):
    __tablename__ = "users"
    login        = ActiveApp.getDB().Column(ActiveApp.getDB().Text,primary_key=True)
    name         = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    surname      = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    password     = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    group_user   = ActiveApp.getDB().relationship("Groups",secondary=group_user,lazy="subquery",back_populates="group_user")
    cosecha_user = ActiveApp.getDB().relationship("Cosecha",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")
    
    def __repr__(self) -> str:
        return f'<login: {self.login}\npassword: {self.password}\ngroup_user:{self.group_user}\ncosecha_user:{self.cosecha_user}>'


class Persona(ActiveApp.getDB().Model):
    __tablename__ = "persona"
    name          = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    surname       = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    CI            = ActiveApp.getDB().Column(ActiveApp.getDB().Text,primary_key=True)
    localPhone    = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    cellPhone     = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    dir1          = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    dir2          = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    persona_productor  = ActiveApp.getDB().relationship("TipoProductor",secondary=productor,lazy="subquery",back_populates="persona_productor")

    def __repr__(self) -> str:
        return f'<name: {self.name}\tsurname: {self.surname}\tCI:{self.CI}\tpersona_productor:{self.persona_productor}>\n'


class TipoProductor(ActiveApp.getDB().Model):
    __tablename__ = "tipo_productor"
    description       = ActiveApp.getDB().Column(ActiveApp.getDB().Text,primary_key=True)
    ID                = ActiveApp.getDB().Column(ActiveApp.getDB().Integer, unique=True)
    persona_productor = ActiveApp.getDB().relationship("Persona",secondary=productor,lazy="subquery",back_populates="persona_productor")
    

class Cosecha(ActiveApp.getDB().Model):
    __tablename__ = "cosecha"
    start_date = ActiveApp.getDB().Column(ActiveApp.getDB().Date,primary_key=True)
    end_date   = ActiveApp.getDB().Column(ActiveApp.getDB().Date,primary_key=True)

    cosecha_user = ActiveApp.getDB().relationship("Users",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")

    def __repr__(self) -> str:
        return f'<start_date: {str(self.start_date)}\nend_date: {str(self.end_date)}'





ActiveApp.getDB().create_all()