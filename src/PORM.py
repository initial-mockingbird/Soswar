from __future__ import annotations
from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, Union, TypedDict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
from src.DB_Model import Cosecha, Encrypt, Persona, Users, Groups, group_user, TipoProductor
from src.DB_Model import productor
from init import ActiveApp
from pymaybe import maybe
from datetime import date, MINYEAR, MAXYEAR
import re
from flask_wtf import FlaskForm


class FieldInfo(TypedDict):
    valueType : type
    modifiable : bool

class UserControlAPI():

    class Control():
        @staticmethod
        def addUser(user : Users) -> None:
            ActiveApp.getDB().session.add(user)
            ActiveApp.getDB().session.commit()

        @staticmethod
        def deleteUser(user : Union[str,Users]) -> None:
            if (isinstance(user,str)):
                Users.query.filter_by(login=user).delete()
            else:
                maybe(user).delete()
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
    
    class Data():
        @staticmethod
        def lookupUser(login : Optional[str]) -> Optional[Users]:
            if login is None or login == "":
                return Users.query.all()
            return Users.query.filter_by(login=login).first()

        @staticmethod
        def incrementalRegexLookup(regex : str) -> List[Users]:
            return [ u for u in Users.query.all() if re.match(regex.strip(),u.login) ]

        @staticmethod
        def incrementalSearch(initPart : str) -> List[Users]:
            return UserControlAPI.Data.incrementalRegexLookup(f"{initPart.strip()}(.)*")

        
class UserViewAPI():
    @staticmethod
    def pFields() -> Dict[str,FieldInfo]:
        fields = {}
        fields['login']        = {'valueType':str,'modifiable':False,'label': 'Login'}
        fields['name']         = {'valueType':str,'modifiable':True,'label':'Nombres'}
        fields['surname']      = {'valueType':str,'modifiable':True,'label':'Apellidos'}
        fields['group_user']   = {'valueType':List[str],'modifiable':True,'label':'Grupo'}
        fields['cosecha_user'] = {'valueType':List[str],'modifiable':True,'label':'Cosecha'}
        return fields
    
    @staticmethod
    def userPublicInfo(login : Optional[str] = None) -> Union[Dict[str,Any],List[Dict[str,Any]]]:
        if (login is not None):
            ret  = {}
            user = UserControlAPI.Data.lookupUser(login)
            for field in UserViewAPI.pFields().keys():
                ret[field] = getattr(user,field)
        else:
            ret = []
            users = Users.query.all()
            for user in users:
                userFields  = {}
                for field in UserViewAPI.pFields().keys():
                    userFields[field] = getattr(user,field)
                ret.append(userFields)

        return ret
    
    class Parse():
        months : Dict[str,int] = {
            "Ene":1,
            "Feb":2,
            "Mar":3,
            "Abr":4,
            "May":5,
            "Jun":6,
            "Jul":7,
            "Ago":8,
            "Sep":9,
            "Oct":10,
            "Nov":11,
            "Dic":12
        }

        @staticmethod
        def parseLogin(login : str) -> str:
            return login

        @staticmethod
        def parseName(name : str) -> str:
            return name
        
        @staticmethod
        def parseSurname(surname : str) -> str:
            return surname
        
        @staticmethod
        def parseGroup(groupName : Union[str,None]) -> List[Groups]:
            if groupName is None or groupName == "":
                return []
            g = Groups.query.filter_by(group=groupName).first()
            if (g and g is not None):
                return [g]
            else:
                return []

        @staticmethod
        def parseDate(dt : str |None) -> List[Cosecha]:
            if dt is None or dt == "":
                return []
            (_,m1,_,m2,y) = dt.split(sep=" ")
            m1_ = UserViewAPI.Parse.months[m1]
            m2_ = UserViewAPI.Parse.months[m2]
            y2_ = int(y)
            if (m1_ >= m2_):
                y1_ = y2_-1
            else:
                y1_ = y2_
            
            d1 = date(y1_,m1_,1)
            d2 = date(y2_,m2_,1)
            return Cosecha.query.filter_by(start_date=d1,end_date=d2).all()


class GroupControlAPI():
    class Control():
        @staticmethod
        def addGroup(group : Groups) -> None:
            ActiveApp.getDB().session.add(group)
            ActiveApp.getDB().session.commit()
              
        @staticmethod
        def deleteGroup(group : Groups) -> None:
            group.delete()
            ActiveApp.getDB().session.commit()
        
        @staticmethod
        def addGroupToUser(group : Union[str,Groups], user : Union[str,Users]) -> None:
            UserControlAPI.Control.addGroupToUser(group,user)
            ActiveApp.getDB().session.commit()
    
    class Data():
        @staticmethod
        def lookupGroup(group : Optional[str]) -> Union[Optional[Groups],List[Groups]]:
            if group is None or group == "":
                return Groups.query.all()    
            return Groups.query.filter_by(group=group).first()
        

class CosechaControlAPI():
    class Control():
        @staticmethod
        def addCosecha(cosecha : Cosecha) -> None:
            ActiveApp.getDB().session.add(cosecha)
            ActiveApp.getDB().session.commit()
        @staticmethod
        def deleteCosecha(cosecha : Cosecha) -> None:
            cosecha.delete()
            ActiveApp.getDB().session.commit()
        
        @staticmethod
        def addCosechaToUser(cosecha : Cosecha, user : Union[str,Users]) -> None:
            UserControlAPI.Control.addCosechaToUser(cosecha,user)
    
    class Data():
        @staticmethod
        def lookupCosecha(ID : Union[str,int,None]) -> Optional[Cosecha]:
            if isinstance(ID,str):
                ID = int(ID)
            return Cosecha.query.filter_by(ID=ID).first()

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


class CosechaViewAPI():
    @staticmethod
    def pFields() -> Dict[str,FieldInfo]:
        fields = {}
        fields['ID']           = {'valueType':str,'modifiable':False,'label':'ID'}
        fields['description']  = {'valueType':str,'modifiable':True ,'label':'Descripcion'}
        fields['start_date']   = {'valueType':str,'modifiable':True ,'label':'Inicio'}
        fields['end_date']     = {'valueType':str,'modifiable':True ,'label':'Cierre'}
        return fields
    
    @staticmethod
    def cosechaPublicInfo(ID : Optional[str] = None) -> Union[Dict[str,Any],List[Dict[str,Any]]]:
        if (ID is not None):
            ret  = {}
            cosecha = CosechaControlAPI.Data.lookupCosecha(ID)
            for field in CosechaViewAPI.pFields().keys():
                ret[field] = getattr(cosecha,field)
        else:
            ret = []
            cosechas = Cosecha.query.all()
            for cosecha in cosechas:
                cosechaFields  = {}
                for field in CosechaViewAPI.pFields().keys():
                    cosechaFields[field] = getattr(cosecha,field)
                ret.append(cosechaFields)

        return ret


def mkForm(pfields : Dict[str, FieldInfo],pInfo,form : FlaskForm):
    for field in pfields:
        properties = {}
        containerAttrs = {}
        if (not pfields[field]['modifiable']):
            properties['readonly '] = 'readonly'
        if (pfields[field]['valueType'] == str):
            properties['value'] = pInfo[field]
            properties['class'] = 'stringBox'
        else:
            properties['class'] = 'defaultBox'
            aux = pInfo[field][0] if pInfo[field] != [] else "" 
            setattr(getattr(form,field),'default',aux)
        
        setattr(getattr(form,field),'render_kw',properties)
        setattr(getattr(form,field),'containerAttrs',containerAttrs)
    form.process()

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
    def addPerson( d:Dict[str,str], ciPersona:str="" ) -> int:
        if ciPersona!="": 
            p = Persona.query.filter_by(CI=ciPersona).first()
        else:
            p = Persona()
            # La cedula no debe existir
            if( Persona.query.filter_by(CI=d['CI']).first() is not None ):
                return 1
            
        fields = AdminAPI.personaPublicFields()

        # La cedula debe tener un formato correcto
        if re.search("[V,J,E](-\d)",d['CI'])==None:
            return 2
        
        # El numero local debe tener un formato correcto
        if re.search("\d{4}(-\d{7})", d['localPhone'])==None:
            return 3
        
        # El numero celular debe tener un formato correcto
        if re.search("\d{4}(-\d{7})", d['cellPhone'])==None:
            return 4
        
        # Caso de input valido
        for field in fields:
            if field != 'persona_productor':
                setattr( p, field, d[field] )
            else:
                valor = [AdminAPI.getTypeOfProducers(d['persona_productor'])]
                setattr( p, field, valor )

        ActiveApp.getDB().session.add(p)
        ActiveApp.getDB().session.commit()
        return 0
    
    @staticmethod
    def addTypeOfProducer( d:Dict[str,str], relations ) -> int:
        tipo = TipoProductor()
        fields = AdminAPI.typeOfProducerPublicFields()

        if (TipoProductor.query.filter_by(description = d['description']).first() is not None):
            return 1

        for field in fields:
            setattr( tipo, field, d[field] )
        tipo.persona_productor = relations

        ActiveApp.getDB().session.add(tipo)
        ActiveApp.getDB().session.commit()
        return 0

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
    def deletePersona(ciPersona : str) -> int:
        p = Persona.query.filter_by(CI=ciPersona)
        if( p.first() is None ):
            return 1

        # only delete 1 element in the relation
        t = p.first().persona_productor[0].persona_productor
        filtered = filter(lambda p2: p2.CI!=ciPersona, t)
        p.first().persona_productor[0].persona_productor = list(filtered) 
        
        p.delete()
        ActiveApp.getDB().session.commit()
        return 0

    @staticmethod
    def deleteTypeOfProducer(name : str) -> int:
        t = TipoProductor.query.filter_by(description=name)
        if( t.first() is None ):
            return 1

        # delete all the persons related with t
        for p in t.first().persona_productor:
            p.persona_productor = []
        
        t.delete()
        ActiveApp.getDB().session.commit()
        return 0
    
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
            for field in UserViewAPI.pFields().keys():
                ret[field] = getattr(user,field)
        else:
            ret = []
            users = Users.query.all()
            for user in users:
                userFields  = {}
                for field in UserViewAPI.pFields().keys():
                    userFields[field] = getattr(user,field)
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


