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
    #RFC del certificado de pruebas Test/resources/b64CSD.txt.
    rfc = "EKU9003173C9"
    #RFC genérico sin comprobantes pendientes en la cuenta.
    rfcNotFound = "XAXX010101000"
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
    
    def testPendings_auth(self):
        pendings = Pendings(self.url, None, self.user, self.password)
        response = pendings.pendings(self.rfc)
        self.assertTrue(self.expected == response.get_status())
        
    def testPendings(self):
        pendings = Pendings(self.url, self.token)
        response = pendings.pendings(self.rfc)
        self.assertTrue(self.expected == response.get_status())

    #UT de Error
    def testPendings_rfcNotFound(self):
        pendings = Pendings(self.url, self.token)
        response = pendings.pendings(self.rfcNotFound)
        self.assertIsNotNone(response.get_status())

    def testPendings_invalidToken(self):
        pendings = Pendings(self.url, "token-invalido")
        response = pendings.pendings(self.rfc)
        self.assertTrue(self.expectedError == response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPendings)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
