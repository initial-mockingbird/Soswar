from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union, TypedDict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
from src.DB_Model import Cosecha, Encrypt, Users, Groups, group_user
from init import ActiveApp
from pymaybe import maybe
from datetime import date, MINYEAR, MAXYEAR
import re
from src.forms import ModifyUserForm

class FieldInfo(TypedDict):
    valueType : type
    modifiable : bool



class User():
    @staticmethod
    def addUser(user : Users) -> bool:
        if (not Users.query.filter_by(login=user.login).first()):
            ActiveApp.getDB().session.add(user)
            ActiveApp.getDB().session.commit()
            return True
        
        return False

    @staticmethod
    def deleteUser(user : Union[str,Users]) -> None:
        if (isinstance(user,str)):
            Users.query.filter_by(login=user).delete()
        else:
            maybe(user).delete()
        ActiveApp.getDB().session.commit()
    
    @staticmethod
    def lookupUser(login : str) -> Optional[Users]:
        return Users.query.filter_by(login=login).first()

    @staticmethod
    def incrementalRegexLookup(regex : str) -> List[Users]:
        return [ u for u in Users.query.all() if re.match(regex.strip(),u.login) ]

    @staticmethod
    def incrementalSearch(initPart : str) -> List[Users]:
        return User.incrementalRegexLookup(f"{initPart.strip()}(.)*")


class AdminAPI():    
    
    @staticmethod
    def addGroup(group : Groups) -> None:
        if (not Groups.query.filter_by(group=group.group).first()):
            ActiveApp.getDB().session.add(group)
            ActiveApp.getDB().session.commit()
    
    @staticmethod
    def addUser(user : Users) -> None:
        if (not Users.query.filter_by(login=user.login).first()):
            ActiveApp.getDB().session.add(user)
            ActiveApp.getDB().session.commit()

    @staticmethod
    def addCosecha(cosecha : Cosecha) -> None:
        if (not Cosecha.get(cosecha)):
            ActiveApp.getDB().session.add(cosecha)
            ActiveApp.getDB().session.commit()

    @staticmethod
    def deleteUser(user : Union[str,Users]) -> None:
        if (isinstance(user,str)):
            Users.query.filter_by(login=user).delete()
        else:
            maybe(user).delete()
        ActiveApp.getDB().session.commit()

    @staticmethod
    def deleteGroup(group : Groups) -> None:
        group.delete()
        ActiveApp.getDB().session.commit()

    @staticmethod
    def addGroupToUser(group : Union[str,Groups], user : Union[str,Users]) -> None:

        if (isinstance(group,str)):
            group = Users.query.filter_by(group=group).first()

        if (isinstance(user,str)):
            user = Users.query.filter_by(login=user).first()

        if (group is not None):
            maybe(user).group_user.append(group)
        
        ActiveApp.getDB().session.commit()

    @staticmethod
    def addCosechaToUser(cosecha : Cosecha, user : Union[str,Users]) -> None:

        if (isinstance(user,str)):
            user = Users.query.filter_by(login=user).first()

        maybe(user).cosecha_user.append(cosecha)
        ActiveApp.getDB().session.commit()
    
    @staticmethod
    def deleteCosecha(cosecha : Cosecha) -> None:
        maybe(Cosecha).query.get(cosecha).delete()
        ActiveApp.getDB().session.commit()

    @staticmethod
    def cosechasInRange(begin : Optional[date] = None,end : Optional[date] = None):
        if (begin is None):
            begin = date(MINYEAR,1,1)
        if (end is None):
            end = date(MAXYEAR,12,31)

        return Cosecha.query.filter(Cosecha.start_date >= begin and Cosecha.end_date <= end).all() 

    @staticmethod
    def cosechas(u : Union[str,Users,None] = None) -> List[Cosecha]:
        if (u is None):
            return Cosecha.query.all()
        if (isinstance(u,str)):
            return maybe(Users).query.filter_by(login=u).first().cosecha_user.or_else([])
        else:
            return u.cosecha_user

    @staticmethod
    def lookupUser(login : str) -> Optional[Users]:
        return Users.query.filter_by(login=login).first()
    
    @staticmethod
    def lookupGroup(group : str) -> Optional[Groups]:
        return Groups.query.filter_by(group=group).first()


    @staticmethod
    def getAllUsers() -> List[Users]:
        return Users.query.all()

    @staticmethod
    def userPublicFields() -> Dict[str,type]:
        fields = {}
        fields['login']   = str
        fields['name']    = str
        fields['surname'] = str
        fields['group_user'] = str
        #return {'login':str,'name':str,'surname':str,'group_user':Groups,'cosecha_user':Cosecha}
        return fields

    @staticmethod
    def pFields() -> Dict[str,FieldInfo]:
        fields = {}
        fields['login']   = {'valueType':str,'modifiable':False,'label': ModifyUserForm().login.label}
        fields['name']    = {'valueType':str,'modifiable':True,'label':ModifyUserForm().name.label}
        fields['surname'] = {'valueType':str,'modifiable':True,'label':ModifyUserForm().surname.label}
        fields['group_user']   = {'valueType':List[str],'modifiable':True,'label':ModifyUserForm().group_user.label}
        fields['cosecha_user'] = {'valueType':List[str],'modifiable':True,'label':ModifyUserForm().cosecha_user.label}
        #return {'login':str,'name':str,'surname':str,'group_user':Groups,'cosecha_user':Cosecha}
        return fields
    
    @staticmethod
    def userPublicInfo(login : Optional[str] = None) -> Union[Dict[str,Any],List[Dict[str,Any]]]:
        if (login is not None):
            ret  = {}
            user = Users.query.filter_by(login=login).first()
            for field in AdminAPI.pFields().keys():
                ret[field] = getattr(user,field)
        else:
            ret = []
            users = Users.query.all()
            for user in users:
                userFields  = {}
                for field in AdminAPI.pFields().keys():
                    userFields[field] = getattr(user,field)
                ret.append(userFields)

        
        return ret