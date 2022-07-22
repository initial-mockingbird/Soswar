from init import ActiveApp
import unittest
import datetime
ActiveApp.test()

from datetime import *
from src.PORM import *
from src.DB_Model import *
from random import randint
from flask import redirect,request, make_response, Response
ActiveApp.getDB().create_all()


with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
    with c.session_transaction() as sess:
        sess['login'] = 'a  dmin'
        sess['password'] = 'admin'
    resp = make_response(redirect('/'))
    resp.set_cookie('login', 'admin')
    resp.set_cookie('password', 'admin')
    admin_group = Groups(group="admin")
    admin_user = Users(
        login = "admin",
        name  = "admin",
        surname = "admin",
        password="admin",
        )
    GroupControlAPI.Control.addGroup(admin_group)
    UserControlAPI.Control.addUser(admin_user)
    GroupControlAPI.Control.addGroupToUser(admin_group,admin_user)

class UniqueCosechaId():
    __unique = 0
    @staticmethod
    def getUniqueId() -> int:
        unique : int = UniqueCosechaId.__unique
        UniqueCosechaId.__unique += 1
        return unique

class UniqueDate():
    __start : datetime = datetime(1000,1,1)
    __end   : datetime = datetime(2000,1,1)

    @staticmethod
    def getUniqueStartDate() -> datetime:
        start : datetime = UniqueDate.__start
        UniqueDate.__start += timedelta(days=1)
        return start
    
    @staticmethod
    def getUniqueEndDate() -> datetime:
        end : datetime = UniqueDate.__end
        UniqueDate.__end += timedelta(days=1)
        return end

class UniqueDescription():
    __unique = 1
    @staticmethod
    def getUniqueDescription() -> str:
        unique : int = UniqueDescription.__unique
        UniqueDescription.__unique += 1
        return str(unique)

class CosechaUniques():
    @staticmethod
    def getUniqueCosecha(is_enabled : bool = True):
        return Cosecha(
            start_date=UniqueDate.getUniqueStartDate(),
            end_date=UniqueDate.getUniqueEndDate(),
            ID=UniqueCosechaId.getUniqueId(),
            description=UniqueDescription.getUniqueDescription(),
            is_enabled=is_enabled
            )

class UserUniques():
    @staticmethod
    def getUniqueUser():
        return Users(
            login=UniqueDescription.getUniqueDescription(),
            password="123456",
            name=UniqueDescription.getUniqueDescription(),
            surname=UniqueDescription.getUniqueDescription()
        )

class GroupUniques():
    @staticmethod
    def getUniqueGroup():
        return Groups(group=UniqueDescription.getUniqueDescription())

class InsertionTestCases(unittest.TestCase):


    def testAddUser(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            UserControlAPI.Control.addUser(UserUniques.getUniqueUser())
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)
    
    def testAddGroup(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            GroupControlAPI.Control.addGroup(GroupUniques.getUniqueGroup())
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)
    
    def testAddGroupToUser(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            user  = UserUniques.getUniqueUser()
            group = GroupUniques.getUniqueGroup()
            GroupControlAPI.Control.addGroup(group)
            UserControlAPI.Control.addUser(user)
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            UserControlAPI.Control.addGroupToUser(group,user)
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)
    
    def testAddCosechaToUser(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            user  = UserUniques.getUniqueUser()
            cosecha = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha(cosecha)
            UserControlAPI.Control.addUser(user)
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            CosechaControlAPI.Control.addCosechaToUser(cosecha,user)
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def esqueleto(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def testAddCosecha(self):
        """Test case for adding a Cosecha that should be acepted by the API"""

        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            cosecha1 = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha( cosecha1 )
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def testAssociateToUser(self):
        """Test case for adding a Cosecha to a user"""

        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            cosecha1 = CosechaUniques.getUniqueCosecha()
            user1    = UserUniques.getUniqueUser() 
            CosechaControlAPI.Control.addCosecha( cosecha1 )
            UserControlAPI.Control.addUser(user1)
            CosechaControlAPI.Control.addCosechaToUser(cosecha1,user1)
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def testAddCompra(self):
        """Test case for adding a Compra that should be acepted by the API"""

        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            logs_before = len(LoggerControlAPI.Data.lookupLog())

            cosecha1 = Cosecha( 
                start_date = datetime(2022, 1, 1),
                end_date = datetime(2022, 2, 2),
                ID = 1000,
                description = "ss",
                is_enabled = True,
            )
            CosechaControlAPI.Control.addCosecha( cosecha1 )

            d1 = {
                'ID' : 2,
                'date' : datetime(2022, 1, 1),
                'CI' : 'V-123234',
                'clase_cacao' : 'tipo1',
                'precio' : 1,
                'cantidad' : 100,
                'humedadPer' : 1,
                'mermaPer' : 1,
                'clase_cacao' : 'clase1',
                'observaciones' : 'xdddd',
                'cosecha_ID' : 1,
                'is_green' : True
            } 
            CompraControlAPI.Control.addCompra( Compra(**d1) ) 
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)


class DeletionTestCases(unittest.TestCase): 

    def testDeleteGroup(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            group = GroupUniques.getUniqueGroup()
            GroupControlAPI.Control.addGroup(group)
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            GroupControlAPI.Control.deleteGroup(group)
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def testDeleteCosecha(self):
        """Test case for Deleting a Cosecha. Does not check for integrity of the rest of the Cosechas"""


        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            for _ in range(20):
                cosecha1 = CosechaUniques.getUniqueCosecha()
                CosechaControlAPI.Control.addCosecha( cosecha1 )
            
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            cosechas = CosechaControlAPI.Data.cosechas()
            lc       = len(cosechas)
            cosecha1 = cosechas[randint(0,lc-1)]
            CosechaControlAPI.Control.deleteCosecha( cosecha1 )
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def testDeleteCompra(self):
        """Test case for delete a Compra that should be acepted by the API"""
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            # Add the Compra to be deleted
            d1 = {
                'ID' : 200,
                'date' : datetime(2022, 1, 1),
                'CI' : 'V-123234',
                'clase_cacao' : 'tipo1',
                'precio' : 1,
                'cantidad' : 100,
                'humedadPer' : 1,
                'mermaPer' : 1,
                'clase_cacao' : 'clase1',
                'observaciones' : 'xdddd',
                'cosecha_ID' : 1,
                'is_green' : True
            } 
            CompraControlAPI.Control.addCompra( Compra(**d1) ) 
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            CompraControlAPI.Control.deleteCompra( 200 ) 
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

    def testDeleteUser(self):
        with ActiveApp.getApp().test_request_context('/') ,ActiveApp.getApp().test_client() as c:
            with c.session_transaction() as sess:
                sess['login'] = 'a  dmin'
                sess['password'] = 'admin'
            resp = make_response(redirect('/'))
            resp.set_cookie('login', 'admin')
            resp.set_cookie('password', 'admin')
            
            user = UserUniques.getUniqueUser()
            UserControlAPI.Control.addUser(user)
            logs_before = len(LoggerControlAPI.Data.lookupLog())
            UserControlAPI.Control.deleteUser(user)
            logs_after = len(LoggerControlAPI.Data.lookupLog())
            assert(logs_before < logs_after)

if __name__ == "__main__":
    unittest.main() # run all tests

