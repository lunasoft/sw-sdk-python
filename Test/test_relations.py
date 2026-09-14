import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from Test.base import SdkTestCase
from Relations.Relations import Relations

class TestRelations(SdkTestCase):
    passwordCsd = config.PASSWORD_CSD
    uuidNotFound = config.ID_NOT_FOUND
    rfc = config.RFC
    uuidCfdi = config.UUID_RELACIONES

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
