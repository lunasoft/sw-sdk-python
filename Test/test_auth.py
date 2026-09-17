import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test.base import SdkTestCase
from Auth.Auth import Auth

class TestAuth(SdkTestCase):
    #La autenticación se ejercita con usuario y contraseña, no necesita token.
    requeridas = ("SDKTEST_USER", "SDKTEST_PASSWORD")

    #UT Autenticación
    def testAuth_success(self):
        auth = Auth(self.url, None , self.user, self.password)
        response = auth.authentication()
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_token(),"El valor de token esta vacio")

    def testAuth_expiration(self):
        auth = Auth(self.url, None , self.user, self.password)
        response = auth.authentication()
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_time_expire(),"El valor de expiration esta vacio")

    #UT de Error
    def testAuth_emailError(self):
        auth = Auth(self.url, None , self.user, "wrongPassword")
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

    def testAuth_userError(self):
        auth = Auth(self.url, None , "usuario.inexistente@example.com", self.password)
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

    def testAuth_emptyCredentials(self):
        auth = Auth(self.url, None , "", "")
        response = auth.authentication()
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message(),"El valor de message esta vacio")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuth)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
