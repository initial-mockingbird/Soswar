from __future__ import annotations
from ast import In
from dataclasses import field
from typing import Any, Callable, Dict, List, Optional, Union, TypedDict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, backref
from src.DB_Model import Cosecha, Encrypt, Persona, Users, Groups, group_user, TipoProductor, Compra
from src.DB_Model import productor
from init import ActiveApp
from pymaybe import maybe,Maybe,Something
from datetime import date, MINYEAR, MAXYEAR
import re
from flask_wtf import FlaskForm


setattr(Maybe,'fmap',lambda _1,_2: maybe(None))
setattr(Something,'fmap',lambda self,f: maybe(f(self.get())))
setattr(Maybe,'and_then',lambda _1,_2: maybe(None))
setattr(Something,'and_then',lambda self,f: f(self.get()))



def loadFakeData(): 
    # Load in the DB an admin
    g = Groups(group="admin")
    GroupControlAPI.Control.addGroup(g)
    u = Users(login="admin_user",password=Encrypt.encrypt("admin_user"), name="Pedro", surname="Perez",group_user=[g])
    UserControlAPI.Control.addUser(u)

    # Load in the DB an analist 
    g = Groups(group="analist")
    GroupControlAPI.Control.addGroup(g)
    u = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto",group_user=[g])
    UserControlAPI.Control.addUser(u)

    # Load type of producer
    AdminAPI.addTypeOfProducer({'ID':1, 'description':"casa", 'precio':1},[]) 

    # Load a Cosecha
    cosecha1 = Cosecha( 
            start_date = date(2022, 1, 1),
            end_date = date(2022, 2, 2),
            ID = 1,
            description = "ss",
            is_enabled = True,
        )
    CosechaControlAPI.Control.addCosecha( cosecha1 )

    # Load a Compra in Cosecha 1 
    d1 = {
        'ID' : 2,
        'date' : date(2022, 1, 1),
        'CI' : 'V-123234',
        'clase_cacao' : 'tipo1',
        'precio' : 1.2,
        'cantidad' : 30,
        'humedadPer' : 8,
        'mermaPer' : 1.0,
        'observaciones' : 'xdddd',
        'cosecha_ID' : 1,
    } 
    ans = CompraControlAPI().Control().addCompra( Compra(**d1) ) 

    # Load a Compra in Cosecha 1 
    d1 = {
        'ID' : 3,
        'date' : date(2022, 1, 1),
        'CI' : 'V-123234',
        'clase_cacao' : 'tipo1',
        'precio' : 1.2,
        'cantidad' : 30,
        'humedadPer' : 8,
        'mermaPer' : 1.0,
        'observaciones' : 'xdddd',
        'cosecha_ID' : 1,
    } 
    ans = CompraControlAPI().Control().addCompra( Compra(**d1) ) 


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
        def parseCosecha(description : str | None) -> List[Cosecha]:
            return maybe(CosechaControlAPI.Data.lookupCosechaD(description)).fmap(lambda x: [x]).or_else([])

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
            Cosecha.query.filter_by(ID=cosecha.ID).delete()
            #cosecha.delete()
            ActiveApp.getDB().session.commit()
        
        @staticmethod
        def addCosechaToUser(cosecha : Cosecha, user : Union[str,Users]) -> None:
            UserControlAPI.Control.addCosechaToUser(cosecha,user)
    
    class Data():
        @staticmethod
        def lookupCosecha(ID : Union[str,int,None]) -> Optional[Cosecha] | List[Cosecha]:
            if isinstance(ID,str):
                ID = int(ID)
            return Cosecha.query.filter_by(ID=ID).first()

        @staticmethod
        def lookupCosechaD(description : Union[str,None]) -> Optional[Cosecha]:
            return Cosecha.query.filter_by(description=description).first()

        @staticmethod
        def cosechasInRange(begin : Optional[date] = None,end : Optional[date] = None):
            if (begin is None):
                begin = date(MINYEAR,1,1)
            if (end is None):
                end = date(MAXYEAR,12,31)

            return Cosecha.query.filter(Cosecha.start_date >= begin, Cosecha.end_date <= end).all() 

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
        fields['is_enabled']   = {'valueType':bool,'modifiable':True ,'label':'Habilitada?'}
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


class CompraControlAPI():
    class Control():
        @staticmethod
        def addCompra( c : Compra ) -> int:
            # The compra['ID'] can't exist
            if( Compra.query.filter_by(ID=c.ID).first() is not None ):
                return 1 

            # Check the correct format of the CI
            if re.search("[V,J,E](-\d)",c.CI)==None:
                return 2
            
            ActiveApp.getDB().session.add(c)
            ActiveApp.getDB().session.commit()
            return 0

        @staticmethod
        def deleteCompra(compraID : Compra) -> None:
            p = Compra.query.filter_by(ID=compraID)

            # The CompraID, have to be in the db
            if( p.first() is None ): return 1

            p.delete() 
            ActiveApp.getDB().session.commit()
            return 0
        
        @staticmethod
        def updateCompra( d:Dict[str,str] ) -> None:
            # The compra['ID'] have to exist
            if( Compra.query.filter_by(ID=d['ID']).first() is None ):
                return 1
            
            # Check the correct format of the CI
            if re.search("[V,J,E](-\d)",d['CI'])==None:
                return 2
            
            # We get the Buyer
            c = Compra.query.filter_by(ID=d['ID']).first()
            # And also the list of fiels
            fields = CompraControlAPI().Data().pFields()
            
            # Update manually each field
            for field in fields: setattr( c, field, d[field] )
            
            ActiveApp.getDB().session.add(c)
            ActiveApp.getDB().session.commit()
            return 0

    class Data():
        @staticmethod
        def pFields() -> Dict[str,FieldInfo]:
            fields = {}
            fields['ID']          = {'valueType':int, 'modifiable':False,'label': 'Login'}
            fields['date']        = {'valueType':date,'modifiable':True, 'label':'Nombres'}
            fields['CI']          = {'valueType':str, 'modifiable':True, 'label':'Apellidos'}
            fields['precio']      = {'valueType':int, 'modifiable':True, 'label':'Grupo'}
            fields['clase_cacao'] = {'valueType':str, 'modifiable':True, 'label':'Grupo'}
            fields['cantidad']    = {'valueType':int, 'modifiable':True, 'label':'Cosecha'}
            fields['humedadPer']  = {'valueType':int, 'modifiable':True, 'label':'Cosecha'}
            fields['mermaPer']    = {'valueType':int, 'modifiable':True, 'label':'Cosecha'}
            fields['observaciones'] = {'valueType':str,'modifiable':True, 'label':'Cosecha'}
            fields['cosecha_ID']  = {'valueType':int, 'modifiable':True, 'label':'Cosecha'} 
            fields['recolector_ID'] = {'valueType':int,'modifiable':True,'label':'Cosecha'} 
            return fields
        
        @staticmethod
        def fieldsUI () -> Dict[str,FieldInfo]:
            # The order imply the in the UI
            columnWidth = [ 120, 150, 150, 150, 150, 200, 200, 200, 200, 200, 200, 200, 200, 200 ]
            fields = {}
            fields['ID']       = {'valueType':int,'modifiable':False,'label': 'ID', 'width':70}
            fields['date']     = {'valueType':date,'modifiable':True,'label':'Fecha', 'width':150}
            fields['CI']       = {'valueType':str,'modifiable':True,'label':'Cedula', 'width':130}
            fields['precio']   = {'valueType':int,'modifiable':True,'label':'Precio ($)', 'width':150}
            fields['clase_cacao']   = {'valueType':str,'modifiable':True,'label':'Clase de cacao', 'width':150}
            fields['cantidad'] = {'valueType':int,'modifiable':True,'label':'Cantidad (kg)', 'width':150}
            fields['humedadPer'] = {'valueType':int,'modifiable':True,'label':'Humedad (%)', 'width':150}
            fields['mermaPer']   = {'valueType':int,'modifiable':True,'label':'Merma (%)', 'width':150}
            fields['merma']   = {'valueType':int,'modifiable':True,'label':'Merma (kg)', 'width':150}
            fields['cantidad_total']   = {'valueType':int,'modifiable':True,'label':'Cantidad total (kg)', 'width':170}
            fields['monto']   = {'valueType':int,'modifiable':True,'label':'Monto ($)', 'width':150}
            fields['observaciones'] = {'valueType':str,'modifiable':True,'label':'observaciones', 'width':150}
            fields['cosecha_ID'] = {'valueType':int,'modifiable':True,'label':'Cosecha ID', 'width':150} 
            fields['recolector_ID'] = {'valueType':int,'modifiable':True,'label':'Recolector ID', 'width':150}
            return fields
        

        @staticmethod
        def lookupCompra( compraID:int=None ) -> List[Compra]|Compra:
            if compraID==None:
                compras = Compra.query.all()
            else: 
                compras = Compra.query.filter_by(ID=compraID).first()
            return compras
            


def mkForm(pfields : Dict[str, FieldInfo],pInfo,form : FlaskForm):
    for field in pfields:
        properties = {}
        containerAttrs = {}
        if (not pfields[field]['modifiable']):
            properties['readonly '] = 'readonly'
            properties['class'] = f"{properties.get('class','')} disabled"
        if (pfields[field]['valueType'] == str):
            properties['value'] = pInfo[field]
            properties['class'] = f"{properties.get('class','')} stringBox"
        else:
            properties['class'] = f"{properties.get('class','')} defaultBox"
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
        return [ 'ID','description', 'precio' ]

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


