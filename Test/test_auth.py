import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Auth.Auth import Auth

class TestAuth(unittest.TestCase):
    expected = "success"
    message = "307. El comprobante contiene un timbre previo."
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    def testAuth(self):
        auth = Auth("http://services.test.sw.com.mx", None , os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = auth.authentication()
        self.assertTrue(self.expected == response.get_status())
    

suite = unittest.TestLoader().loadTestsFromTestCase(TestAuth)
unittest.TextTestRunner(verbosity=2).run(suite)
