import unittest
import os
import sys

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Balance.Balance import Balance

class TestBalance(unittest.TestCase):
    expected = "success"
    
    def testBalance_auth(self):
        balance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        response = balance.get_balance()
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        self.assertIsNotNone(response.data.idUser)
        self.assertIsNotNone(response.data.idUserBalance)
        self.assertIsNotNone(response.data.stampsAssigned)
        self.assertIsNotNone(response.data.stampsUsed)
        self.assertIsNotNone(response.data.stampsBalance)
        
    def testBalance(self):
        balance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = balance.get_balance()
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        self.assertIsNotNone(response.data.idUser)
        self.assertIsNotNone(response.data.idUserBalance)
        self.assertIsNotNone(response.data.stampsAssigned)
        self.assertIsNotNone(response.data.stampsUsed)
        self.assertIsNotNone(response.data.stampsBalance)
        
    @unittest.skip("Evitar conflictos por temas de saldos")
    def testBalance_add_auth(self):
        balance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = balance.add_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Prueba Pyhton")
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        print(response.get_data())
        
    @unittest.skip("Evitar conflictos por temas de saldos")
    def testBalance_add(self):
        balance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = balance.add_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Prueba Pyhton")
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        print(response.get_data())
        
    @unittest.skip("Evitar conflictos por temas de saldos")
    def testBalance_remove_auth(self):
        balance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = balance.remove_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Prueba Pyhton")
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        print(response.get_data())
      
    @unittest.skip("Evitar conflictos por temas de saldos")  
    def testBalance_remove(self):
        balance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = balance.remove_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Prueba Pyhton")
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
        print(response.get_data())

suite = unittest.TestLoader().loadTestsFromTestCase(TestBalance)
unittest.TextTestRunner(verbosity=2).run(suite)
