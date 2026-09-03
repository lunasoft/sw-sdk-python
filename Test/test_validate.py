import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Validate.Validate import Validate

class TestValidate(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    user = os.environ.get("SDKTEST_USER")
    password = os.environ.get("SDKTEST_PASSWORD")
    token = os.environ.get("SDKTEST_TOKEN")

    @classmethod
    def setUpClass(cls):
        for nombre, valor in (("SDKTEST_USER", cls.user),
                              ("SDKTEST_PASSWORD", cls.password),
                              ("SDKTEST_TOKEN", cls.token)):
            if not valor:
                raise ValueError(f"Falta la variable de entorno {nombre}")

    @staticmethod
    def open_file(pathFile):
        with open(pathFile, "r", encoding='utf-8') as file:
            out = file.read()
        return out
    
    def testValidateXml_Auth(self):
        validate = Validate(self.url, None, self.user, self.password)
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"))
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("Vigente"== response.response['statusSat'])
        self.assertEqual("S", response.response['statusCodeSat'].split(" - ")[0])
        
    def testValidateXml(self):
        validate = Validate(self.url, self.token)
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"))
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("Vigente"== response.response['statusSat'])
        self.assertEqual("S", response.response['statusCodeSat'].split(" - ")[0])
        
    def testValidateXml_WithStatus(self):
        validate = Validate(self.url, self.token)
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"),True)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("Vigente"== response.response['statusSat'])
        #statusCodeSat llega como "<código> - <texto>": el texto es del servicio, así que
        #la prueba afirma únicamente el código.
        self.assertEqual("S", response.response['statusCodeSat'].split(" - ")[0])
        
    def testValidateXml_WithoutStatus(self):
        validate = Validate(self.url, self.token)
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"),False)
        self.assertTrue(self.expected == response.get_status())
        self.assertTrue("No Aplica"== response.response['statusSat'])
        self.assertTrue("No Aplica"== response.response['statusCodeSat'])

    #UT de Error
    def testValidateXml_invalidXml(self):
        validate = Validate(self.url, self.token)
        response = validate.ValidateXml("<xml>no es un cfdi</xml>")
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message())

    def testValidateXml_invalidToken(self):
        validate = Validate(self.url, "token-invalido")
        response = validate.ValidateXml(TestValidate.open_file("Test/resources/xml40Stamp.xml"))
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestValidate)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
