import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Pendings.Pendings import Pendings

class TestPendings(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testPendings_auth(self):
        pendings = Pendings("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = pendings.pendings("EKU9003173C9")
        self.assertTrue(self.expected == response.get_status())
        
    def testPendings(self):
        pendings = Pendings("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = pendings.pendings("EKU9003173C9")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(TestPendings)
unittest.TextTestRunner(verbosity=2).run(suite)
