import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Pendings.Pendings import Pendings

class TestPendings(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    @staticmethod
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
    def testPendings_auth(self):
        pendings = Pendings("https://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = pendings.pendings("EKU9003173C9")
        self.assertTrue(self.expected == response.get_status())
        
    def testPendings(self):
        pendings = Pendings("https://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = pendings.pendings("EKU9003173C9")
        self.assertTrue(self.expected == response.get_status())

    #UT de Error
    def testPendings_rfcNotFound(self):
        pendings = Pendings(TestPendings.url, os.environ["SDKTEST_TOKEN"])
        response = pendings.pendings("XAXX010101000")
        self.assertIsNotNone(response.get_status())

    def testPendings_invalidToken(self):
        pendings = Pendings(TestPendings.url, "token-invalido")
        response = pendings.pendings("EKU9003173C9")
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPendings)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
