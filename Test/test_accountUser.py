import unittest
import os
import sys

#Función para poder importar módulos necesarios.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from AccountUser.AccountUser import AccountUser

class TestAccountUser(unittest.TestCase):
    expected = "success"
     
    @unittest.skip("Se omite para evitar afectar UT")
    def testAccountUser_create_user_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        name = "Prueba UT Hijo Python"
        taxId = "XAXX010101000"
        email = f"userPython_{os.environ['SDKTEST_USER']}"
        password = f"_{os.environ['SDKTEST_PASSWORD']}"
        notificationEmail = f"user_{os.environ['SDKTEST_USER']}"
        phone = "0000000000"
        response = accountUser.create_user(name,taxId,email,1,False,password,notificationEmail,phone)
        message_expect = f"El email '{email}' ya esta en uso."
        self.assertTrue(self.expected == response.get_status() or message_expect == response.get_message())
        
    @unittest.skip("Se omite para evitar afectar UT")
    def testAccountUser_update_user_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        idUser = "b9e42c65-4afa-45a2-9b0d-d67b1373a7f4"
        name = "Prueba UT Hijo Python Actualizado"
        taxId = "XAXX010101002"
        phone = "0000000001"
        response = accountUser.update_user(idUser,name,taxId,None,phone,False)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(idUser == response.get_data())
        
    def testAccountUser_all_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        response = accountUser.getUser_all()
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.data.items) > 0)
    
    def testAccountUser_by_idUser_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        idUser = "32501CF2-DC62-4370-B47D-25024C44E131"
        response = accountUser.getUser_by_idUser(idUser)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.data.items) > 0) 
        for user in response.data.items:
            print("\tName: ",user.name)
            print("\tIdDelear: ",user.idDealer)
            print("\tIdUser: ",user.idUser)
            print("\t taxId: ",user.taxId)
            print("\t username: ",user.username)
            print("\t email: ",user.email)
            print("\t profile: ",user.profile)
            print("\t isAcrtive: ",user.isActive)
            print("\t accessToken: ",user.accessToken)
            print("\t stamps: ",user.stamps)
            print("\t phone: ",user.phone)
            print("\t isUnlimited: ",user.isUnlimited)
        
    def testAccountUser_by_email_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        email = f"userPython_{os.environ['SDKTEST_USER']}"
        response = accountUser.getUser_by_email(email)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.data.items) > 0) 
        
    def testAccountUser_by_taxId_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        taxId = "AAAA000101010"
        response = accountUser.getUser_by_taxId(taxId)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.data.items) > 0)  
        
    def testAccountUser_by_isActive_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        response = accountUser.getUser_by_isActive(True)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue(len(response.data.items) > 0) 
        
    @unittest.skip("Evitar conflictos por temas de saldos")  
    def testAccountUser_delete_user_auth(self):
        accountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, os.environ['SDKTEST_USER'], os.environ['SDKTEST_PASSWORD'])
        idUser = "8e6ec77d-b4d6-47aa-95b9-89b354d8207b"
        response = accountUser.delete_user(idUser)
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_data())
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountUser)
unittest.TextTestRunner(verbosity=2).run(suite)