from sqlalchemy import Column, Date, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
import hashlib
from typing import Any
from init import ActiveApp
from datetime import datetime,date 
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
    ActiveApp.getDB().Column('cosecha',ActiveApp.getDB().Integer,ActiveApp.getDB().ForeignKey('cosecha.ID'),primary_key=True),
    )

productor = ActiveApp.getDB().Table("productor",
    ActiveApp.getDB().Model.metadata,
    ActiveApp.getDB().Column('CI',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('persona.CI'),primary_key=True),
    ActiveApp.getDB().Column('description',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('tipo_productor.description'),primary_key=True)
    )

class Groups(ActiveApp.getDB().Model):
    __tablename__ = "groups"

    def __init__(self,**kwargs) -> None:
        super().__init__()
        for (k,v) in kwargs.items():
            getattr(self,k)
            setattr(self,k,v)
        ActiveApp.getDB().session.commit()

    group = ActiveApp.getDB().Column(ActiveApp.getDB().Text,primary_key=True)
    group_user = ActiveApp.getDB().relationship("Users",secondary=group_user,lazy="subquery",back_populates="group_user")

    def __repr__(self) -> str:
        return f'{self.group}'


class Users(ActiveApp.getDB().Model):
    __tablename__ = "users"

    def __init__(self,**kwargs) -> None:
        super().__init__()
        for (k,v) in kwargs.items():
            getattr(self,k)
            setattr(self,k,v)
        ActiveApp.getDB().session.commit()
    
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

    def __repr__(self) -> str:
        return f'<description: {self.description}\nID: {self.ID}\npersona_productor:{self.persona_productor}>\n'
    

class Cosecha(ActiveApp.getDB().Model):
    __tablename__ = "cosecha"

    def __init__(self,**kwargs) -> None:
        super().__init__()
        for (k,v) in kwargs.items():
            getattr(self,k)
            setattr(self,k,v)
        ActiveApp.getDB().session.commit()

    start_date  = ActiveApp.getDB().Column(ActiveApp.getDB().Date,nullable=False)
    end_date    = ActiveApp.getDB().Column(ActiveApp.getDB().Date,nullable=False)
    ID         = ActiveApp.getDB().Column(ActiveApp.getDB().Integer,primary_key=True)
    description = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    cosecha_user = ActiveApp.getDB().relationship("Users",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")

    def __repr__(self) -> str:
        meses  = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
        return f'Cosecha {meses[self.start_date.month-1]} - {meses[self.end_date.month-1]} {self.end_date.year}'







ActiveApp.getDB().create_all()