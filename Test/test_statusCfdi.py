import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from StatusCfdi.StatusCfdi import StatusCfdi

class TestStatusCfdi(unittest.TestCase):
    urlProd="https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc"
    soapAction = "http://tempuri.org/IConsultaCFDIService/Consulta"

    def testStatusCfdi(self):
        objStatus = StatusCfdi.status("CAU180123GEA", "GACM650215GH9", "398.39", "699628be-2f06-4bc9-adc2-860b51eecbca", self.urlProd, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.codigoEstatus)
        self.assertIsNotNone(objStatus.esCancelable)
        self.assertIsNotNone(objStatus.estado)

    def testStatusCfdi_notFound(self):
        #Un UUID que no existe responde igual con 200, con el codigo de estatus del SAT.
        objStatus = StatusCfdi.status("CAU180123GEA", "GACM650215GH9", "398.39",
                                      "00000000-0000-0000-0000-000000000000", self.urlProd, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.codigoEstatus)

    def testStatusCfdi_totalDistinto(self):
        objStatus = StatusCfdi.status("CAU180123GEA", "GACM650215GH9", "1.00",
                                      "699628be-2f06-4bc9-adc2-860b51eecbca", self.urlProd, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.codigoEstatus)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatusCfdi)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
