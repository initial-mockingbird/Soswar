from sqlalchemy import null
from init import ActiveApp
import unittest
import datetime
ActiveApp.test()

from datetime import date
from src.PORM import *
from src.DB_Model import *

ActiveApp.getDB().create_all()

class UniqueId():
    __unique = 0

    @staticmethod
    def getUniqueId() -> str:
        unique : int = UniqueId.__unique
        UniqueId.__unique += 1
        return str(unique)

class InsertionTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.compraAPI = CompraControlAPI()
        self.control = self.compraAPI.Control()
        
    # All cases for adding Compras

    def testAddCompra(self):
        """Test case for adding a Compra that should be acepted by the API"""

        cosecha1 = Cosecha( 
            start_date = datetime(2022, 1, 1),
            end_date = datetime(2022, 2, 2),
            ID = 1,
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
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==0 )
        
    def testAddCompraBadCI1(self):
        """Test case for adding a Compra with bad CI"""

        d1 = {
            'ID' : 3,
            'date' : datetime(2022, 1, 1),
            'CI' : '123234',
            'clase_cacao' : 'tipo1',
            'precio' : 1,
            'cantidad' : 100,
            'humedadPer' : 1,
            'mermaPer' : 1,
            'clase_cacao' : 'clase1',
            'observaciones' : 'xdddd',
            'cosecha_ID' : 1,
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==2 )

    def testAddCompraBadCI2(self):
        """Test case for adding a Compra with bad CI"""
        
        d1 = {
            'ID' : 3,
            'date' : datetime(2022, 1, 1),
            'CI' : 'A-123234',
            'clase_cacao' : 'tipo1',
            'precio' : 1,
            'cantidad' : 100,
            'humedadPer' : 1,
            'mermaPer' : 1,
            'clase_cacao' : 'clase1',
            'observaciones' : 'xdddd',
            'cosecha_ID' : 1,
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==2 )

    def testAddCompraBadCI3(self):
        """Test case for adding a Compra with bad CI"""
        
        d1 = {
            'ID' : 3,
            'date' : datetime(2022, 1, 1),
            'CI' : 'V-',
            'clase_cacao' : 'tipo1',
            'precio' : 1,
            'cantidad' : 100,
            'humedadPer' : 1,
            'mermaPer' : 1,
            'clase_cacao' : 'clase1',
            'observaciones' : 'xdddd',
            'cosecha_ID' : 1,
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==2 )

    def testAddCompraBadCI4(self):
        """Test case for adding a Compra with bad CI"""
        
        d1 = {
            'ID' : 3,
            'date' : datetime(2022, 1, 1),
            'CI' : 'V 123234',
            'clase_cacao' : 'tipo1',
            'precio' : 1,
            'cantidad' : 100,
            'humedadPer' : 1,
            'mermaPer' : 1,
            'clase_cacao' : 'clase1',
            'observaciones' : 'xdddd',
            'cosecha_ID' : 1,
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==2 )

    def testAddCompraRepeatCI(self):
        """Test case for adding a Compra with bad CI"""
        
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
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==1 )

class DeletionTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.compraAPI = CompraControlAPI()
        self.control = self.compraAPI.Control()
        
    # All cases for delete Compras

    def testDeleteCompra(self):
        """Test case for delete a Compra that should be acepted by the API"""
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
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==0 )
        
        ans = self.control.deleteCompra( 200 ) 
        assert( ans==0 )

    def testDeleteCompraNotExist(self):
        """Test case for delete a Compra that should isn't in the db"""
        ans = self.control.deleteCompra( 100000 ) 
        assert( ans==1 )

class SearchTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.compraAPI = CompraControlAPI()
        self.control = self.compraAPI.Control()
        self.dataCompra = self.compraAPI.Data()
        
    # All cases for search Compras

    def testLookupCompra(self):
        """Test case for search a Compra in the db"""
        # Add the Compra to be deleted
        d1 = {
            'ID' : 10,
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
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==0 ) 
        
        obj = self.dataCompra.lookupCompra( 10 )
        assert( obj.ID==10 )

    def testLookupCompraNotExit(self):
        """Test case for search a Compra in the db"""
        # Add the Compra to be deleted
        
        obj = self.dataCompra.lookupCompra( 99 )
        assert( obj==None )

    def testLookupCompraAll(self):
        """Test case for search a Compra in the db"""
        # Add the Compra to be deleted
        
        lista = self.dataCompra.lookupCompra(  )
        assert( len(lista)==2 )
        assert( lista[0].ID==2 )
        assert( lista[1].ID==10 )
    
class UpdateTestCases(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.compraAPI = CompraControlAPI()
        self.control = self.compraAPI.Control()
        self.dataCompra = self.compraAPI.Data()
        
    # All cases for update Compras

    def testUpdateCompra(self):
        """Test case for update a Compra in the db"""
        # Add a compra
        d1 = {
            'ID' : 777,
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
            'recolector_ID' : 1
        } 
        ans = self.control.addCompra( Compra(**d1) ) 
        assert( ans==0 )

        # Dictionary needed for update
        d1 = {
            'ID' : 777,
            'date' : datetime(2022, 1, 1),
            'CI' : 'V-123234',
            'clase_cacao' : 'tipo1',
            'precio' : 2,
            'cantidad' : 100,
            'humedadPer' : 1,
            'mermaPer' : 1,
            'clase_cacao' : 'clase1',
            'observaciones' : 'xdddd',
            'cosecha_ID' : 1,
            'recolector_ID' : 1
        } 

        # Search and verify
        obj = self.dataCompra.lookupCompra( 777 ) 

        # Update the object with ID 10
        assert( obj.precio==1.0 )
        ans = self.control.updateCompra( d1 )

        # Search and verify
        obj = self.dataCompra.lookupCompra( 777 ) 
        assert( obj.precio==2.0 )
        


if __name__ == "__main__":
    unittest.main() # run all tests

