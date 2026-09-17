import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from Test.base import SdkTestCase
from CancelationRetentions.CancelationRetentions import CancelationRetentions

class TestCancelationRetentions(SdkTestCase):
    passwordCsd = config.PASSWORD_CSD
    rfc = config.RFC
    uuidCfdi = config.UUID_CANCELACION_RETENCION

    def testCancelXml_auth(self):
        cancel = CancelationRetentions(self.url, None, self.user, self.password)
        response = cancel.cancel_xml(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelXml(self):
        cancel = CancelationRetentions(self.url, self.token)
        response = cancel.cancel_xml(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelCsd_auth(self):
        cancel = CancelationRetentions(self.url, None, self.user, self.password)
        response = cancel.cancel_csd(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64CSD.txt"), TestCancelationRetentions.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelCsd(self):
        cancel = CancelationRetentions(self.url, self.token)
        response = cancel.cancel_csd(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64CSD.txt"), TestCancelationRetentions.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelPfx_auth(self):
        cancel = CancelationRetentions(self.url, None, self.user, self.password)
        response = cancel.cancel_pfx(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelPfx(self):
        cancel = CancelationRetentions(self.url, self.token)
        response = cancel.cancel_pfx(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    #UT de Error
    def testCancelRetentions_invalidToken(self):
        #CancelationRetentionsResponse tampoco asigna status cuando el servicio no
        #responde 200, así que la prueba afirma el código y el mensaje.
        cancel = CancelationRetentions(self.url, "token-invalido")
        response = cancel.cancel_xml(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(401 == response.get_status_code())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCancelationRetentions)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
