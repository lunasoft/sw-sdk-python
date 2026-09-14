import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from Test.base import SdkTestCase
from Pendings.Pendings import Pendings

class TestPendings(SdkTestCase):
    rfc = config.RFC
    rfcInvalid = config.RFC_INVALID

    def testPendings_auth(self):
        pendings = Pendings(self.url, None, self.user, self.password)
        response = pendings.pendings(self.rfc)
        self.assertTrue(self.expected == response.get_status())
        
    def testPendings(self):
        pendings = Pendings(self.url, self.token)
        response = pendings.pendings(self.rfc)
        self.assertTrue(self.expected == response.get_status())

    #UT de Error
    def testPendings_invalidRfc(self):
        #XAXX010101000 no sirve como caso sin coincidencias: la cuenta de pruebas tiene
        #comprobantes pendientes con ese RFC. Un RFC mal formado si responde error.
        pendings = Pendings(self.url, self.token)
        response = pendings.pendings(self.rfcInvalid)
        self.assertTrue(self.expectedError == response.get_status())
        self.assertTrue(400 == response.get_status_code())
        self.assertIsNotNone(response.get_message())

    def testPendings_invalidToken(self):
        pendings = Pendings(self.url, "token-invalido")
        response = pendings.pendings(self.rfc)
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPendings)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
