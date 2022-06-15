from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
import hashlib
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

productor_user = ActiveApp.getDB().Table("productor_user",
    ActiveApp.getDB().Model.metadata,
    ActiveApp.getDB().Column('login',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('users.login'),primary_key=True),
    ActiveApp.getDB().Column('ID',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('productor.ID'),primary_key=True)
    )

cosecha_user = ActiveApp.getDB().Table("cosecha_user",
    ActiveApp.getDB().Model.metadata,
    ActiveApp.getDB().Column('login',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('users.login'),primary_key=True),
    ActiveApp.getDB().Column('cosecha',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('cosecha.start_date'),primary_key=True),
    ActiveApp.getDB().Column('cosecha',ActiveApp.getDB().Text,ActiveApp.getDB().ForeignKey('cosecha.end_date'),primary_key=True)
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
    CI           = ActiveApp.getDB().Column(ActiveApp.getDB().Text,nullable=False)
    localPhone   = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    cellPhone    = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    dir1         = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    dir2         = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    group_user   = ActiveApp.getDB().relationship("Groups",secondary=group_user,lazy="subquery",back_populates="group_user")
    cosecha_user = ActiveApp.getDB().relationship("Cosecha",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")
    productor_user = ActiveApp.getDB().relationship("Productor",secondary=productor_user,lazy="subquery",back_populates="productor_user")
    def __repr__(self) -> str:
        return f'<login: {self.login}\npassword: {self.password}\ngroup_user:{self.group_user}\ncosecha_user:{self.cosecha_user}>'


class Productor(ActiveApp.getDB().Model):
    __tablename__ = "productor"
    ID          = ActiveApp.getDB().Column(ActiveApp.getDB().Integer,primary_key=True)
    description = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    dir1         = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    dir2         = ActiveApp.getDB().Column(ActiveApp.getDB().Text)
    productor_user = ActiveApp.getDB().relationship("Users",secondary=productor_user,lazy="subquery",back_populates="productor_user")



class Cosecha(ActiveApp.getDB().Model):
    __tablename__ = "cosecha"
    start_date = ActiveApp.getDB().Column(ActiveApp.getDB().Date,primary_key=True)
    end_date   = ActiveApp.getDB().Column(ActiveApp.getDB().Date,primary_key=True)

    cosecha_user = ActiveApp.getDB().relationship("Users",secondary=cosecha_user,lazy="subquery",back_populates="cosecha_user")

    def __repr__(self) -> str:
        return f'<start_date: {str(self.start_date)}\nend_date: {str(self.end_date)}'


ActiveApp.getDB().create_all()