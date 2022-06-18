from __future__ import annotations
from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, Union
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
from src.DB_Model import Cosecha, Encrypt, Persona, Users, Groups, group_user, TipoProductor
from src.DB_Model import productor
from init import ActiveApp
from pymaybe import maybe
from datetime import date, MINYEAR, MAXYEAR

class AdminAPI():    
    
    # Add functions
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
    def addPerson( d:Dict[str,str], ciPersona:str="" ) -> None:
        if ciPersona!="": 
            p = Persona.query.filter_by(CI=ciPersona).first()
        else:
            p = Persona()
        fields = AdminAPI.personaPublicFields()

        for field in fields:
            if field != 'persona_productor':
                setattr( p, field, d[field] )
            else:
                valor = [AdminAPI.getTypeOfProducers(d['persona_productor'])]
                setattr( p, field, valor )

        ActiveApp.getDB().session.add(p)
        ActiveApp.getDB().session.commit()

    @staticmethod
    def addTypeOfProducer( d:Dict[str,str], relations ) -> None:
        tipo = TipoProductor()
        fields = AdminAPI.typeOfProducerPublicFields()

        for field in fields:
            setattr( tipo, field, d[field] )
        tipo.persona_productor = relations

        ActiveApp.getDB().session.add(tipo)
        ActiveApp.getDB().session.commit()


    # Delete functions
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
    def deleteCosecha(cosecha : Cosecha) -> None:
        maybe(Cosecha).query.get(cosecha).delete()
        ActiveApp.getDB().session.commit()

    @staticmethod
    def deletePersona(ciPersona : str) -> None:
        p = Persona.query.filter_by(CI=ciPersona)

        # only delete 1 element in the relation
        t = p.first().persona_productor[0].persona_productor
        filtered = filter(lambda p2: p2.CI!=ciPersona, t)
        p.first().persona_productor[0].persona_productor = list(filtered) 
        
        p.delete()
        ActiveApp.getDB().session.commit()

    @staticmethod
    def deleteTypeOfProducer(name : str) -> None:
        t = TipoProductor.query.filter_by(description=name)

        # delete all the persons related with t
        for p in t.first().persona_productor:
            p.persona_productor = []
        
        t.delete()
        ActiveApp.getDB().session.commit()
    
    # Query functions
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
    def userPublicInfo(login : Optional[str] = None) -> Union[Dict[str,Any],List[Dict[str,Any]]]:
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
                    userFields[field] = str(getattr(user,field))
                ret.append(userFields)

        
        return ret

    @staticmethod
    def personaPublicFields() -> List[str]:
        return [ 'CI','surname','name','localPhone','cellPhone','persona_productor','dir1','dir2' ]

    @staticmethod
    def typeOfProducerPublicFields() -> List[str]:
        return [ 'ID','description' ]

    @staticmethod
    def getAllPersonas( filterCI:str=None ) -> List[Dict[str,Any]]:
        if filterCI == None:
            personas = Persona.query.all()
        else:
            personas = Persona.query.filter_by(CI=filterCI)
        
        # Transform list of persons to list of list for a better speed acces
        fields = AdminAPI.personaPublicFields()
        ans = [ [ getattr(p,field) for field in fields ] for p in personas ]
        for p in ans:
            if len(p[5])>0:
                p[5] = p[5][0].description 
        return ans 
    
    @staticmethod
    def getAllTypeOfProducers( filterDesctiption:str=None ) -> List[TipoProductor]:
        if filterDesctiption==None:
            productores = TipoProductor.query.all()
        else: 
            productores = TipoProductor.query.filter_by(description=filterDesctiption)
        fields  = AdminAPI.typeOfProducerPublicFields()
        return [ [ getattr(p,field) for field in fields ] for p in productores ]
    
    @staticmethod
    def getTypeOfProducers( des:str ) -> TipoProductor:
        return TipoProductor.query.filter_by(description=des).first()

    @staticmethod
    def updPerson( ciPersona : str, d : Dict[str,str]) -> None:
        if ciPersona!=d['CI']:
            AdminAPI.deletePersona( ciPersona )
            AdminAPI.addPerson( d )
        else:
            AdminAPI.addPerson( d, ciPersona )

    @staticmethod
    def updTypeOfProducer( name : str, d : Dict[str,str]) -> None:
        # Save relacions
        t = TipoProductor.query.filter_by(description=name)
        relations = t.first().persona_productor

        # Delete and add
        AdminAPI.deleteTypeOfProducer( name ) 
        AdminAPI.addTypeOfProducer( d, relations )


