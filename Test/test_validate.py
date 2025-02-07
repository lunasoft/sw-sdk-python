import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Validate.Validate import Validate

class TestValidate(unittest.TestCase):
    expected = "success"
    @staticmethod
    def open_file(pathFile):
        out = open(pathFile, "r", encoding='ansi', errors='ignore').read()
        return out
    
    def testValidateXml_Auth(self):
        validate = Validate("http://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testValidateXml(self):
        validate = Validate("http://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40.xml"))
        self.assertTrue(self.expected == response.get_status())

suite = unittest.TestLoader().loadTestsFromTestCase(TestValidate)
unittest.TextTestRunner(verbosity=2).run(suite)
