import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Auth.Auth import Auth

class TestAuth(unittest.TestCase):
    expectedSucces = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    
    #Las credenciales de la cuenta de pruebas nunca van en el codigo.
    user = os.environ.get("SDKTEST_USER")
    password = os.environ.get("SDKTEST_PASSWORD")

    @classmethod
    def setUpClass(cls):
        for nombre, valor in (("SDKTEST_USER", cls.user),
                              ("SDKTEST_PASSWORD", cls.password)):
            if not valor:
                raise ValueError(f"Falta la variable de entorno {nombre}")

    def testAuth_success(self):
        auth = Auth(self.url, None , self.user, self.password)
        response = auth.authentication()
        self.assertTrue(self.expectedSucces == response.get_status())
        self.assertIsNotNone(response.get_token(),"El valor de token esta vacio")
        
    def testAuth_emailError(self):
        auth = Auth(self.url, None , self.user, "wrongPassword")
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

    def testAuth_expiration(self):
        auth = Auth(TestAuth.url, None , self.user, self.password)
        response = auth.authentication()
        self.assertTrue(self.expectedSucces == response.get_status())
        self.assertIsNotNone(response.get_time_expire(),"El valor de expiration esta vacio")

    def testAuth_userError(self):
        auth = Auth(TestAuth.url, None , "usuario.inexistente@example.com", self.password)
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

    def testAuth_emptyCredentials(self):
        auth = Auth(TestAuth.url, None , "", "")
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuth)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
