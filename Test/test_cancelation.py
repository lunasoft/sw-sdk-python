import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Cancelation.Cancelation import Cancelation

class TestCancelation(unittest.TestCase):
    expected = "success"
    url = "https://services.test.sw.com.mx"
    #Contraseña del CSD público de pruebas del SAT, no de una cuenta: se puede
    #sobrescribir con SDKTEST_CSD_PASSWORD.
    passwordCsd = os.environ.get("SDKTEST_CSD_PASSWORD", "12345678a")
    #RFC del certificado de pruebas Test/resources/b64CSD.txt.
    rfc = "EKU9003173C9"
    #CFDI timbrado en la cuenta de pruebas sobre el que se ejercita la cancelación.
    uuidCfdi = "3dda215e-4c77-4923-94a1-627e0a04378c"
    #Las credenciales de la cuenta de pruebas nunca van en el código.
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
    
    #UT de Cancelación
    def testCancelXml_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.CancelXml(TestCancelation.open_file("Test/resources/cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelXml(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.CancelXml(TestCancelation.open_file("Test/resources/cancelByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelCsd_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.CancelCsd(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64CSD.txt"), TestCancelation.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelCsd(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.CancelCsd(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64CSD.txt"), TestCancelation.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelPfx_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.CancelPfx(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelPfx(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.CancelPfx(self.uuidCfdi, self.rfc, TestCancelation.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelUuid_auth(self):
        cancel = Cancelation(self.url, None, self.user, self.password)
        response = cancel.CancelUuid(self.uuidCfdi, self.rfc, "02", "")
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelUuid(self):
        cancel = Cancelation(self.url, self.token)
        response = cancel.CancelUuid(self.uuidCfdi, self.rfc, "02", "")
        self.assertTrue(self.expected == response.get_status())

    #UT de Error
    def testCancelUuid_invalidToken(self):
        #CancelationResponse no asigna status cuando el servicio no responde 200, así que
        #la prueba afirma el código y el mensaje, que es el comportamiento real de hoy.
        cancel = Cancelation(self.url, "token-invalido")
        response = cancel.CancelUuid(self.uuidCfdi, self.rfc, "02", "")
        self.assertTrue(401 == response.get_status_code())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCancelation)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
