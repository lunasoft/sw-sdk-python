import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Csd.Csd import Csd

class TestCsd(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testUploadCsd_auth(self):
        csd_obj = Csd("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())
        
    def testUploadCsd(self):
        csd_obj = Csd("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = csd_obj.upload_csd("stamp", TestCsd.open_file("Test/resources/b64CSD.txt"), TestCsd.open_file("Test/resources/b64Key.txt"),"12345678a")
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(TestCsd)
unittest.TextTestRunner(verbosity=2).run(suite)
