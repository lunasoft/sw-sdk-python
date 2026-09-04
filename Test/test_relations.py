import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Relations.Relations import Relations

class TestRelations(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    #Contraseña del CSD público de pruebas del SAT, se sobrescribe con SDKTEST_CSD_PASSWORD.
    passwordCsd = os.environ.get("SDKTEST_CSD_PASSWORD", "12345678a")
    uuidNotFound = "00000000-0000-0000-0000-000000000000"
    #RFC del certificado de pruebas Test/resources/b64CSD.txt.
    rfc = "EKU9003173C9"
    #CFDI timbrado en la cuenta de pruebas del que se consultan las relaciones.
    uuidCfdi = "316dff4d-6a5a-40d5-8558-c8f45244aa90"
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
    
    #UT Consulta de relaciones
    def testRelationsCsd_auth(self):
        relations = Relations(self.url, None, self.user, self.password)
        response = relations.relations_csd(self.rfc,self.uuidCfdi,TestRelations.open_file("Test/resources/b64CSD.txt"), TestRelations.open_file("Test/resources/b64Key.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testRelationsCsd(self):
        relations = Relations(self.url, self.token)
        response = relations.relations_csd(self.rfc,self.uuidCfdi,TestRelations.open_file("Test/resources/b64CSD.txt"), TestRelations.open_file("Test/resources/b64Key.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testRelationsPfx_auth(self):
        relations = Relations(self.url, None, self.user, self.password)
        response = relations.relations_pfx(self.rfc,self.uuidCfdi,TestRelations.open_file("Test/resources/b64Pfx.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testRelationsPfx(self):
        relations = Relations(self.url, self.token)
        response = relations.relations_pfx(self.rfc,self.uuidCfdi,TestRelations.open_file("Test/resources/b64Pfx.txt"),self.passwordCsd)
        self.assertTrue(self.expected == response.get_status())
        
    def testRelationsUuid_auth(self):
        relations = Relations(self.url, None, self.user, self.password)
        response = relations.relations_uuid(self.rfc,self.uuidCfdi)
        self.assertTrue(self.expected == response.get_status())
        
    def testRelationsUuid(self):
        relations = Relations(self.url, self.token)
        response = relations.relations_uuid(self.rfc,self.uuidCfdi)
        self.assertTrue(self.expected == response.get_status())

    #UT Consultas sin coincidencias
    def testRelationsUuid_notFound(self):
        #Un UUID sin relaciones responde success con el aviso en message, no es un error.
        relations = Relations(self.url, self.token)
        response = relations.relations_uuid(self.rfc, self.uuidNotFound)
        self.assertTrue(self.expected == response.get_status())
        self.assertIsNotNone(response.get_message())

    #UT de Error
    def testRelationsUuid_invalidToken(self):
        relations = Relations(self.url, "token-invalido")
        response = relations.relations_uuid(self.rfc, self.uuidCfdi)
        self.assertTrue(self.expectedError == response.get_status())
        self.assertTrue(401 == response.get_status_code())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRelations)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
