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
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
    def testValidateXml_Auth(self):
        validate = Validate("https://services.test.sw.com.mx", None, os.environ["SDKTEST_USER"], os.environ["SDKTEST_PASSWORD"])
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"))
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("Vigente"== response.response['statusSat'])
        self.assertTrue("S - Comprobante obtenido satisfactoriamente"== response.response['statusCodeSat'])
        
    def testValidateXml(self):
        validate = Validate("https://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"))
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("Vigente"== response.response['statusSat'])
        self.assertTrue("S - Comprobante obtenido satisfactoriamente"== response.response['statusCodeSat'])
        
    def testValidateXml_WithStatus(self):
        validate = Validate("https://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"),True)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("Vigente"== response.response['statusSat'])
        self.assertTrue("S - Comprobante obtenido satisfactoriamente"== response.response['statusCodeSat'])
        
    def testValidateXml_WithoutStatus(self):
        validate = Validate("https://services.test.sw.com.mx", os.environ["SDKTEST_TOKEN"])
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"),False)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("No Aplica"== response.response['statusSat'])
        self.assertTrue("No Aplica"== response.response['statusCodeSat'])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestValidate)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
