from init import ActiveApp
import unittest
import datetime
ActiveApp.test()

from datetime import *
from src.PORM import *
from src.DB_Model import *
from random import randint
ActiveApp.getDB().create_all()


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

class InsertionTestCases(unittest.TestCase):

    def testAddCosecha(self):
        """Test case for adding a Cosecha that should be acepted by the API"""

        cosecha1 = CosechaUniques.getUniqueCosecha()
        CosechaControlAPI.Control.addCosecha( cosecha1 )
        assert( CosechaControlAPI.Data.lookupCosecha(cosecha1.ID) is not None )
        assert( CosechaControlAPI.Data.lookupCosechaD(cosecha1.description) is not None )

    def testAssociateToUser(self):
        """Test case for adding a Cosecha to a user"""

        cosecha1 = CosechaUniques.getUniqueCosecha()
        user1    = UserUniques.getUniqueUser() 
        CosechaControlAPI.Control.addCosecha( cosecha1 )
        UserControlAPI.Control.addUser(user1)
        CosechaControlAPI.Control.addCosechaToUser(cosecha1,user1)
        
        assert(cosecha1.description in map(lambda x: x.description,user1.cosecha_user))

        
    def testAddCosechaBad1(self):
        """Test case for adding a Cosecha with repeated ID"""

        cosecha1 = CosechaUniques.getUniqueCosecha()
        CosechaControlAPI.Control.addCosecha( cosecha1 )
        cosechas = CosechaControlAPI.Data.cosechas()
        cosecha2 = CosechaUniques.getUniqueCosecha()
        cosecha2.ID = cosecha1.ID
        cosechas_ = CosechaControlAPI.Data.cosechas()
        assert(cosechas == cosechas_)
    
    def testAddCosechaBad2(self):
        """Test case for adding a Cosecha with repeated description"""

        cosecha1 = CosechaUniques.getUniqueCosecha()
        CosechaControlAPI.Control.addCosecha( cosecha1 )
        cosechas = CosechaControlAPI.Data.cosechas()
        cosecha2 = CosechaUniques.getUniqueCosecha()
        cosecha2.description = cosecha1.description
        cosechas_ = CosechaControlAPI.Data.cosechas()
        assert(cosechas == cosechas_)

class DeletionTestCases(unittest.TestCase): 
    def testDeleteCosecha(self):
        """Test case for Deleting a Cosecha. Does not check for integrity of the rest of the Cosechas"""

        for _ in range(20):
            cosecha1 = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha( cosecha1 )
        
        cosechas = CosechaControlAPI.Data.cosechas()
        lc       = len(cosechas)
        cosecha1 = cosechas[randint(0,lc-1)]
        ID = cosecha1.ID
        description = cosecha1.description
        CosechaControlAPI.Control.deleteCosecha( cosecha1 )
        assert( CosechaControlAPI.Data.lookupCosecha(ID) is None )
        assert( CosechaControlAPI.Data.lookupCosechaD(description) is None )
    
    def testDeleteIntegrity(self):
        """Test case for Deleting a Cosecha. Checks Integrity"""

        for _ in range(20):
            cosecha1 = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha( cosecha1 )
        
        cosechas = CosechaControlAPI.Data.cosechas()
        lc       = len(cosechas)
        cosecha1 = cosechas[randint(0,lc-1)]
        CosechaControlAPI.Control.deleteCosecha( cosecha1 )
        lc_ = len(CosechaControlAPI.Data.cosechas())
        assert(lc_ + 1  == lc)

    def testDeleteIntegrity2(self):
        """Test case for Deleting a Cosecha that does not exists. Checks Integrity"""

        for _ in range(20):
            cosecha1 = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha( cosecha1 )
        
        cosechas = CosechaControlAPI.Data.cosechas()
        lc       = len(cosechas)
        cosecha1 = CosechaUniques.getUniqueCosecha()
        CosechaControlAPI.Control.deleteCosecha( cosecha1 )
        lc_ = len(CosechaControlAPI.Data.cosechas())
        assert(lc_  == lc)

class LookupTestCases(unittest.TestCase): 

    def testLookupRanges(self):
        """Test case for Searching Ranges in a Cosecha, not specifying a range should be the same as in returning all Cosecha"""
        for _ in range(20):
            cosecha1 = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha( cosecha1 )
        
        assert(CosechaControlAPI.Data.cosechasInRange() == CosechaControlAPI.Data.cosechas())

    def testLookupRanges2(self):
        """Test case for Searching Ranges in a Cosecha, specifying a range should be the same as a filter Cosecha"""
        for _ in range(20):
            cosecha1 = CosechaUniques.getUniqueCosecha()
            CosechaControlAPI.Control.addCosecha( cosecha1 )
        
        start_date = date(1,1,1)
        end_date   = date(5000,1,1)
        cosechas   = CosechaControlAPI.Data.cosechasInRange(begin=start_date,end=end_date)
        cosechas_  = [c for c in CosechaControlAPI.Data.cosechas() if c.start_date >= start_date and c.end_date <= end_date]
        assert(cosechas == cosechas_)

if __name__ == "__main__":
    unittest.main() # run all tests

