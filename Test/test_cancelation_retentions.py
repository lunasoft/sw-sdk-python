import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Cancelation_Retentions.CancelationRetentions import CancelationRetentions

class TestCancelationRetentions(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
    def testCancelaUno_auth(self):
        cancel = CancelationRetentions("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelaUno(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelaUno(self):
        cancel = CancelationRetentions("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelaUno(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelaUnoCSD_auth(self):
        cancel = CancelationRetentions("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelaUnoCSD("578052ce-710f-4d0b-9ffc-6ca73daf92a5", "EKU9003173C9", TestCancelationRetentions.open_file("Test/resources/b64CSD.txt"), TestCancelationRetentions.open_file("Test/resources/b64Key.txt"),"12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelaUnoCSD(self):
        cancel = CancelationRetentions("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelaUnoCSD("578052ce-710f-4d0b-9ffc-6ca73daf92a5", "EKU9003173C9", TestCancelationRetentions.open_file("Test/resources/b64CSD.txt"), TestCancelationRetentions.open_file("Test/resources/b64Key.txt"),"12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelaUnoPFX_auth(self):
        cancel = CancelationRetentions("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = cancel.CancelaUnoPFX("578052ce-710f-4d0b-9ffc-6ca73daf92a5", "EKU9003173C9", TestCancelationRetentions.open_file("Test/resources/b64Pfx.txt"), "12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelaUnoPFX(self):
        cancel = CancelationRetentions("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = cancel.CancelaUnoPFX("578052ce-710f-4d0b-9ffc-6ca73daf92a5", "EKU9003173C9", TestCancelationRetentions.open_file("Test/resources/b64Pfx.txt"), "12345678a", "02", "")
        self.assertTrue(self.expected == response.get_status())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCancelationRetentions)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
