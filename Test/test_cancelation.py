import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from Test.base import SdkTestCase
from Cancelation.Cancelation import Cancelation

class TestCancelation(SdkTestCase):
    passwordCsd = config.PASSWORD_CSD
    rfc = config.RFC
    uuidCfdi = config.UUID_CANCELACION

    #UT Cancelación
    def testCancelXml_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.cancel_xml(TestCancelation.open_file("Test/resources/cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelXml(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.cancel_xml(TestCancelation.open_file("Test/resources/cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelCsd_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.cancel_csd(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64CSD.txt"), TestCancelation.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelCsd(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.cancel_csd(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64CSD.txt"), TestCancelation.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelPfx_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.cancel_pfx(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelPfx(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.cancel_pfx(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelUuid_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.cancel_uuid(self.uuidCfdi, self.rfc, "02", "")
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelUuid(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.cancel_uuid(self.uuidCfdi, self.rfc, "02", "")
        self.assertTrue(self.expected == response.get_status())

    #UT de Error
    def testCancelUuid_invalidToken(self):
        #CancelationResponse no asigna status cuando el servicio no responde 200, así que
        #la prueba afirma el código y el mensaje.
        cancel = Cancelation(self.url, "token-invalido")
        response = cancel.cancel_uuid(self.uuidCfdi, self.rfc, "02", "")
        self.assertTrue(401 == response.get_status_code())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCancelation)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
