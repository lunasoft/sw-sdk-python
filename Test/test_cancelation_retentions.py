import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Cancelation_Retentions.CancelationRetentions import CancelationRetentions

class TestCancelationRetentions(unittest.TestCase):
    expected = "success"
    url = "https://services.test.sw.com.mx"
    #Contrasena del CSD publico de pruebas del SAT, no de una cuenta: se puede
    #sobrescribir con SDKTEST_CSD_PASSWORD.
    passwordCsd = os.environ.get("SDKTEST_CSD_PASSWORD", "12345678a")
    #RFC del certificado de pruebas Test/resources/b64CSD.txt.
    rfc = "EKU9003173C9"
    #Retencion timbrada en la cuenta de pruebas sobre la que se ejercita la cancelacion.
    uuidCfdi = "578052ce-710f-4d0b-9ffc-6ca73daf92a5"
    #Las credenciales de la cuenta de pruebas nunca van en el codigo.
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
    
    def testCancelaUno_auth(self):
        cancel = CancelationRetentions(self.url, None, self.user, self.password)
        response = cancel.CancelaUno(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelaUno(self):
        cancel = CancelationRetentions(self.url, self.token)
        response = cancel.CancelaUno(TestCancelationRetentions.open_file("Test/resources/cancelRetByXml.xml"))
        self.assertTrue(self.expected == response.get_status())
    
    def testCancelaUnoCSD_auth(self):
        cancel = CancelationRetentions(self.url, None, self.user, self.password)
        response = cancel.CancelaUnoCSD(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64CSD.txt"), TestCancelationRetentions.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelaUnoCSD(self):
        cancel = CancelationRetentions(self.url, self.token)
        response = cancel.CancelaUnoCSD(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64CSD.txt"), TestCancelationRetentions.open_file("Test/resources/b64Key.txt"),self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())
        
    def testCancelaUnoPFX_auth(self):
        cancel = CancelationRetentions(self.url, None, self.user, self.password)
        response = cancel.CancelaUnoPFX(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

    def testCancelaUnoPFX(self):
        cancel = CancelationRetentions(self.url, self.token)
        response = cancel.CancelaUnoPFX(self.uuidCfdi, self.rfc, TestCancelationRetentions.open_file("Test/resources/b64Pfx.txt"), self.passwordCsd, "02", "")
        self.assertTrue(self.expected == response.get_status())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCancelationRetentions)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
