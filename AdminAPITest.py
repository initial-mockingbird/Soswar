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
cosecha1 = Cosecha(start_date=date(2022,3,1),end_date=date(2022,12,1))
cosecha2 = Cosecha(start_date=date(2022,6,1),end_date=date(2022,8,1))
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
        

if __name__ == "__main__":
    unittest.main() # run all tests