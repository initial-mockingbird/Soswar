from init import ActiveApp
import unittest
ActiveApp.test()

from datetime import date
from src.PORM import *
from src.DB_Model import *

ActiveApp.getDB().create_all()
admin_user = Users(login="admin_user",password=Encrypt.encrypt("admin_user"),name="admin name",surname="admin surname")
dan   = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto")
angel = Users(login="angel",password=Encrypt.encrypt("angel"), name="Angel", surname="Garces")

admin = Groups(group="admin")
analist = Groups(group="analist")
cosecha1 = Cosecha(start_date=date(2022,3,1),end_date=date(2022,12,1),ID=1, description="a", is_enabled=True)
cosecha2 = Cosecha(start_date=date(2022,6,1),end_date=date(2022,8,1),ID=2, description="a", is_enabled=True)
admin_user.group_user.append(admin)
dan.group_user.append(analist)
dan.cosecha_user.append(cosecha1)
dan.cosecha_user.append(cosecha2)

ActiveApp.getDB().session.add(admin_user)
ActiveApp.getDB().session.add(analist)
ActiveApp.getDB().session.add(cosecha1)
ActiveApp.getDB().session.add(cosecha2)
ActiveApp.getDB().session.add(dan)
ActiveApp.getDB().session.add(angel)
ActiveApp.getDB().session.commit()

class UniqueId():
    __unique = 0

    @staticmethod
    def getUniqueId() -> str:
        unique : int = UniqueId.__unique
        UniqueId.__unique += 1
        return str(unique)

class SearchTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        import src.DB_Model 
        self.dan = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto")

    def testSearchUserMember(self):
        """Test case for searching a User that belongs in the db."""

        user = AdminAPI.lookupUser(self.dan.login)
        assert(user is not None)
        assert(user.login == self.dan.login)

    def testSearchUserNotMember(self):
        """Test case for searching a User that does NOT belongs in the db."""
        uniqueId : str = UniqueId.getUniqueId()
        user  : Optional[Users] = AdminAPI.lookupUser(uniqueId)
        assert(user is None)

    def testSearchGroupMember(self):
        """Test case for searching a Group that belongs in the db."""
        assert(True)
    
    # All cases for search a typeOfProducer

    def testSearchTOP(self):
        """Test case for searching a Type of producer in the db."""
        # Add a type of producer
        ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':2000, 'description':'productor2000' } ,[])
        assert( ans==0 )

        lista = AdminAPI.getAllTypeOfProducers( 'productor2000' )
        assert( len(lista)==1 )
        assert( lista[0][1]=='productor2000' )
        assert( lista[0][0]==2000 )
    
    def testSearchNotTOP(self):
        """Test case for searching a Type of producer that don't exist in the db."""

        lista = AdminAPI.getAllTypeOfProducers( 'productor2000' )
        assert( len(lista)==0 )
    
    def testSearchAllTheTOP(self):
        """Test case for searching for all the Type of producer in the db."""
        # Add a type of producer
        for i in range(2001,2010):
            descriptionName = 'productor'+str(i)
            ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':i, 'description':descriptionName } ,[])
            assert( ans==0 )

        lista = AdminAPI.getAllTypeOfProducers()
        assert( len(lista)==108 )

    # All cases for search Person

    def testSearchPerson(self):
        """Test case for searching a Person in the db."""
        # Add a type of producer
        ans2 = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':777, 'description':'productor777' } ,[])
        assert( ans2==0 )
        
        # Add person
        d = {}
        d['CI'] = "V-7777777"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor777'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==0 )

        # Look for that person
        lista = AdminAPI.getAllPersonas('V-7777777')
        assert( len(lista)==1 )
        assert( lista[0][0]=='V-7777777' )

    def testSearchNotPerson(self):
        """Test case for searching a Person that don't belongs to the db."""
        
        # Look for that person
        lista = AdminAPI.getAllPersonas('V-1234569999')
        assert( len(lista)==0 )

class InsertionTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.dan = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto")

    def testAddUserMember(self):
        """Test case for adding a User that belongs in the db, should do nothing."""
        user : Optional[Users] = AdminAPI.lookupUser(self.dan.login) # search for good ol dan
        assert(user is not None) # dan is in db, dan must not be none
        oldName = user.name
        overwritten : Users = Users(login=self.dan.login,password=self.dan.password, name="", surname="")

        AdminAPI.addUser(overwritten)

        newUser : Optional[Users] = AdminAPI.lookupUser(overwritten.login)
        assert(newUser is not None)
        assert(oldName == newUser.name)
    
    def testAddUserNotMember(self):
        """Test case for adding a User that does NOT belongs in the db."""
        uniqueId : str = UniqueId.getUniqueId()
        notIn : Users = Users(login=uniqueId,password=uniqueId, name=uniqueId, surname=uniqueId)
        user  : Optional[Users] = AdminAPI.lookupUser(notIn.login)
        assert(user is None)
        AdminAPI.addUser(notIn)
        user   = AdminAPI.lookupUser(notIn.login)
        assert(user is not None)
        assert(user.login == notIn.login)
        
    # All cases for adding a Type of producer

    def testAddTOP(self):
        """Test case for adding a TypeOfProducer that should be acepted by the API"""
        ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':1, 'description':'productor2' } ,[])
        assert( ans==0 )
    
    def testAddTOPwithRepeadDescription(self):
        """Test case for adding a TypeOfProducer that should be acepted by the API"""
        ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':2, 'description':'productor2' } ,[])
        assert( ans==1 )
        
    def testAdd100TOP(self):
        """Test case for adding 100 TypeOfProducers"""

        for i in range(5,100):
            s = 'productor'+str(i)
            ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':i, 'description':s } ,[])
            assert( ans==0 )
        
    # All cases for adding a Producer

    def testAddPerson(self):
        """Test case for adding a Person that should be acepted by the API"""
        ans2 = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':2, 'description':'productor1' } ,[])
        assert( ans2==0 )
        
        d = {}
        d['CI'] = "V-21172237"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor1'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==0 )

    def testAddPersonWithBadCI0(self):
        """Test case for adding a CI already added"""
    
        d = {}
        d['CI'] = "V-21172237"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==1 )

    def testAddPersonWithBadCI1(self):
        """Test case for adding a Person with bad CI"""
    
        d = {}
        d['CI'] = "V-"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==2 )

    def testAddPersonWithBadCI2(self):
        """Test case for adding a Person with bad CI"""
    
        d = {}
        d['CI'] = "12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==2 )

    def testAddPersonWithBadCI3(self):
        """Test case for adding a Person with bad CI"""
    
        d = {}
        d['CI'] = "A-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==2 )

    def testAddPersonWithBadCI4(self):
        """Test case for adding a Person with bad CI"""
    
        d = {}
        d['CI'] = "V12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==2 )

    def testAddPersonWithBadLocalPhone1(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '04149936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==3 )

    def testAddPersonWithBadLocalPhone2(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '041-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==3 )

    def testAddPersonWithBadLocalPhone3(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-AA36220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==3 )

    def testAddPersonWithBadLocalPhone4(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = 'AA00-1136220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==3 )

    def testAddPersonWithBadCellPhone1(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['cellPhone'] = '04149936220'
        d['localPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==4 )

    def testAddPersonWithBadCellPhone2(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['cellPhone'] = '041-9936220'
        d['localPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==4 )

    def testAddPersonWithBadCellPhone3(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['cellPhone'] = '0414-AA36220'
        d['localPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==4 )

    def testAddPersonWithBadCellPhone4(self):
        """Test case for adding a Person with bad local phone"""
    
        d = {}
        d['CI'] = "V-12123"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['cellPhone'] = 'AA00-1136220'
        d['localPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor2'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==4 )

class DeletionTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""

        self.dan = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto")

    def testDeleteUserMember(self):
        """
            Test case for deleting a User that belongs in the db, checks if the user is deleted and nobody
            else is.
        """
        user : Optional[Users] = AdminAPI.lookupUser(self.dan.login)
        oldLogin : map[str]  = map(lambda u: u.login,AdminAPI.getAllUsers())
        
        assert(user is not None)
        userLogin : str = user.login

        AdminAPI.deleteUser(self.dan.login)
        
        user = AdminAPI.lookupUser(userLogin)
        assert(user is None)
        newLogins : map[str]  = map(lambda u: u.login,AdminAPI.getAllUsers())

        for login in oldLogin:
            assert(login == userLogin or login in newLogins)

        self.dan = Users(login="dan",password=Encrypt.encrypt("dan"), name="Daniel", surname="Pinto")

        ActiveApp.getDB().session.add(self.dan)
        ActiveApp.getDB().session.commit()

    def testDeleteUserNotMember(self):
        """
            Test case for deleting a User that belongs in the db, checks if the user is deleted 
            and if nobody else is.
        """
        uniqueId : str = UniqueId.getUniqueId()
        notIn : Users = Users(login=uniqueId,password=uniqueId, name=uniqueId, surname=uniqueId)
        oldLogins : map[str]  = map(lambda u: u.login,AdminAPI.getAllUsers())
        
        AdminAPI.deleteUser(notIn.login)
        newLogins : map[str]  = map(lambda u: u.login,AdminAPI.getAllUsers())

        for login in oldLogins:
            assert(login in newLogins)

        for login in newLogins:
            assert(login in oldLogins)

    # All cases for delete typeOfProducer

    def testDeleteTOP(self):
        """Test case for delete a TypeOfProducer that should be acepted by the API"""
        ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':1, 'description':'productor2' } ,[])
        assert( ans==0 )
    
        ans = AdminAPI.deleteTypeOfProducer( 'productor2' )
        assert( ans==0 )

    def testDeleteTOPNonExist(self):
        """Test case for delete a TypeOfProducer non exist"""
        ans = AdminAPI.deleteTypeOfProducer( 'revendedor' )
        assert( ans==1 )
    
    def testDelete100TOP(self):
        """Test case for delete 100 TypeOfProducers"""

        for i in range(5,100):
            s = 'productor'+str(i)
            ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':i, 'description':s } ,[])
            assert( ans==0 )
        
        for i in range(5,100):
            s = 'productor'+str(i)
            ans = AdminAPI.deleteTypeOfProducer( s )
            assert( ans==0 )
        
     # All cases for delete Person

    def testDeletePerson(self):
        """Test case for delete a Person that should be acepted by the API"""
        ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':666, 'description':'productor666' } ,[])
        assert( ans==0 )
        
        d = {}
        d['CI'] = "V-111111"
        d['surname'] = 'Garcia'
        d['name'] = 'Jose'
        d['localPhone'] = '0414-9936220'
        d['cellPhone'] = '0414-9936220'
        d['persona_productor'] = 'productor666'
        d['dir1'] = 'Av 1'
        d['dir2'] = 'transversal1'
        ans = AdminAPI.addPerson(d)
        assert( ans==0 )

        ans = AdminAPI.deletePersona( 'V-111111' )
        assert( ans==0 )

    def testDeletePersonNonExist(self):
        """Test case for delete a Person that don't exist"""
       
        ans = AdminAPI.deletePersona( 'V-666' )
        assert( ans==1 )
    
    def testDelete100Person(self):
        """Test case for delete 100 Persons"""
        ans = AdminAPI.addTypeOfProducer( {'precio':1, 'ID':999, 'description':'productor999' } ,[])
        assert( ans==0 )
        
        for i in range(1000,1100):
            d = {}
            d['CI'] = "V-"+str(i)
            d['surname'] = 'Garcia'
            d['name'] = 'Jose'
            d['localPhone'] = '0414-9936220'
            d['cellPhone'] = '0414-9936220'
            d['persona_productor'] = 'productor999'
            d['dir1'] = 'Av 1'
            d['dir2'] = 'transversal1'
            ans = AdminAPI.addPerson(d)
            assert( ans==0 )

if __name__ == "__main__":
    unittest.main() # run all tests