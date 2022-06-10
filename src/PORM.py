from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
from src.DB_Model import Cosecha, Encrypt, Users, Groups, group_user
from init import app
from pymaybe import maybe
from datetime import date, MINYEAR, MAXYEAR


class AdminAPI():    

    __db : Optional[SQLAlchemy] = None
    
    @staticmethod
    def isInit() -> bool:
        return AdminAPI.__db is not None 
    

    @staticmethod 
    def initAPI(db : Optional[SQLAlchemy] = None) -> None:
        """ Static access method. """
        if AdminAPI.__db == None:
            if (db is None):
                raise ValueError("db must be provided in order to create an Admin API")
            AdminAPI.__db = db

    @staticmethod
    def addGroup(group : Groups) -> None:
        assert(AdminAPI.isInit())
        if (not Groups.query.filter_by(group=group).first()):
            AdminAPI.__db.session.add(group)
            AdminAPI.__db.session.commit()
    
    @staticmethod
    def addUser(user : Users) -> None:
        assert(AdminAPI.isInit())
        if (not Users.query.filter_by(login=user.login).first()):
            AdminAPI.__db.session.add(user)
            AdminAPI.__db.session.commit()

    @staticmethod
    def addCosecha(cosecha : Cosecha) -> None:
        assert(AdminAPI.isInit())
        if (not Cosecha.get(cosecha)):
            AdminAPI.__db.session.add(cosecha)
            AdminAPI.__db.session.commit()

    @staticmethod
    def deleteUser(user : Union[str,Users]) -> None:
        assert(AdminAPI.isInit())
        if (isinstance(user,str)):
            user = Users.query.filter_by(login=user).first()
        
        maybe(user).delete()

    @staticmethod
    def deleteGroup(group : Groups) -> None:
        assert(AdminAPI.isInit())
        group.delete()

    @staticmethod
    def addGroupToUser(group : Union[str,Groups], user : Union[str,Users]) -> None:
        assert(AdminAPI.isInit())

        if (isinstance(group,str)):
            group = Users.query.filter_by(group=group).first()

        if (isinstance(user,str)):
            user = Users.query.filter_by(login=user).first()

        if (group is not None):
            maybe(user).group_user.append(group)

    @staticmethod
    def addCosechaToUser(cosecha : Cosecha, user : Union[str,Users]) -> None:
        assert(AdminAPI.isInit())

        if (isinstance(user,str)):
            user = Users.query.filter_by(login=user).first()

        maybe(user).cosecha_user.append(cosecha)
    
    @staticmethod
    def deleteCosecha(cosecha : Cosecha) -> None:
        assert(AdminAPI.isInit())
        maybe(Cosecha).query.get(cosecha).delete()

    @staticmethod
    def cosechasInRange(begin : Optional[date] = None,end : Optional[date] = None):
        assert(AdminAPI.isInit())
        if (begin is None):
            begin = date(MINYEAR,1,1)
        if (end is None):
            end = date(MAXYEAR,12,31)

        return Cosecha.query.filter(Cosecha.start_date >= begin and Cosecha.end_date <= end).all() 

    @staticmethod
    def cosechas(u : Union[str,Users,None] = None) -> List[Cosecha]:
        assert(AdminAPI.isInit())
        if (u is None):
            return Cosecha.query.all()
        if (isinstance(u,str)):
            return maybe(Users).query.filter_by(login=u).first().cosecha_user.or_else([])
        else:
            return u.cosecha_user

    @staticmethod
    def lookupUser(login : str) -> Optional[Users]:
        assert(AdminAPI.isInit())
        return Users.query.filter_by(login=login).first()
    
    

    @staticmethod
    def userPublicFields() -> Dict[str,type]:
        assert(AdminAPI.isInit())
        fields = {}
        fields['login']   = str
        fields['name']    = str
        fields['surname'] = str
        #return {'login':str,'name':str,'surname':str,'group_user':Groups,'cosecha_user':Cosecha}
        return fields

    
    @staticmethod
    def userPublicInfo(login : Optional[str] = None) -> Union[Dict[str,Any],List[Dict[str,Any]]]:
        assert(AdminAPI.isInit())
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
