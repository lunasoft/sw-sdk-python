import unittest
import os
import json
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from AcceptReject.AcceptReject import AcceptReject

class TestAcceptReject(unittest.TestCase):
    expected = "success"
    url = "https://services.test.sw.com.mx"
    #Contrasena del CSD publico de pruebas del SAT, no de una cuenta: se puede
    #sobrescribir con SDKTEST_CSD_PASSWORD.
    passwordCsd = os.environ.get("SDKTEST_CSD_PASSWORD", "12345678a")
    #RFC del certificado de pruebas Test/resources/b64CSD.txt.
    rfc = "EKU9003173C9"
    #CFDI recibido en la cuenta de pruebas sobre el que se ejercita la aceptacion.
    uuidCfdi = "baf029f3-93ea-4267-a76c-1958d69bd4d8"
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
    
    def testAcceptRejectCsd_auth(self):
        accept_reject = AcceptReject(self.url, None, self.user, self.password)
        uuids = [{"uuid":self.uuidCfdi, "action":"Rechazo"}]
        response = accept_reject.accept_reject_csd(self.rfc,uuids,TestAcceptReject.open_file("Test/resources/b64CSD.txt"), TestAcceptReject.open_file("Test/resources/b64Key.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
    
    def testAcceptRejectCsd(self):
        accept_reject = AcceptReject(self.url, self.token)
        uuids = [{"uuid":self.uuidCfdi, "action":"Rechazo"}]
        response = accept_reject.accept_reject_csd(self.rfc,uuids,TestAcceptReject.open_file("Test/resources/b64CSD.txt"), TestAcceptReject.open_file("Test/resources/b64Key.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectXml_auth(self):
        accept_reject = AcceptReject(self.url, None, self.user, self.password)
        response = accept_reject.accept_reject_xml(TestAcceptReject.open_file("Test/resources/fileAcceptReject.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectXml(self):
        accept_reject = AcceptReject(self.url, self.token)
        response = accept_reject.accept_reject_xml(TestAcceptReject.open_file("Test/resources/fileAcceptReject.xml"))
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectPfx_auth(self):
        accept_reject = AcceptReject(self.url, None, self.user, self.password)
        uuids = [{"uuid":self.uuidCfdi, "action":"Rechazo"}]
        response = accept_reject.accept_reject_pfx(self.rfc,uuids,TestAcceptReject.open_file("Test/resources/b64Pfx.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectPfx(self):
        accept_reject = AcceptReject(self.url, self.token)
        uuids = [{"uuid":self.uuidCfdi, "action":"Rechazo"}]
        response = accept_reject.accept_reject_pfx(self.rfc,uuids,TestAcceptReject.open_file("Test/resources/b64Pfx.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectUuid_autth(self):
        accept_reject = AcceptReject(self.url, None, self.user, self.password)
        response = accept_reject.accept_reject_uuid(self.rfc,self.uuidCfdi, "Rechazo")
        self.assertTrue(self.expected == response.get_status())
        
    def testAcceptRejectUuid(self):
        accept_reject = AcceptReject(self.url, self.token)
        response = accept_reject.accept_reject_uuid(self.rfc,self.uuidCfdi, "Rechazo")
        self.assertTrue(self.expected == response.get_status())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAcceptReject)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
