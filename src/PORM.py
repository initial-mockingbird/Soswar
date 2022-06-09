from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
from src.DB_Model import Cosecha, Encrypt, Users, db, Groups, group_user
from init import app
from src.DB_Model import Users, db


class AdminAPI():

    @staticmethod
    def addUser(user : Users):
        if (not Users.query.filter_by(login=user.login).first()):
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def cosechas():
        return Cosecha.all()

    @staticmethod
    def lookupUser(login : str):
        return Users.query.filter_by(login=login).first()
    
    @staticmethod
    def deleteUser(login : str):
        Users.query.filter_by(login=login).first().delete()
    

    @staticmethod
    def userPublicFields():
        fields = {}
        fields['login']   = str
        fields['name']    = str
        fields['surname'] = str
        #return {'login':str,'name':str,'surname':str,'group_user':Groups,'cosecha_user':Cosecha}
        return fields

    
    @staticmethod
    def userPublicInfo(login = None):
        
        if (login is not None):
            ret  = {}
            user = Users.query.filter_by(login=login).first()
            for field in AdminAPI.userPublicFields().keys():
                ret[field] = getattr(user,field)
        else:
            ret = []
            users = Users.query.all()
            for user in users:
                userFields  = {}
                for field in AdminAPI.userPublicFields().keys():
                    userFields[field] = getattr(user,field)
                ret.append(userFields)

        
        return ret
