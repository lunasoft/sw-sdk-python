import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from StatusCfdi.StatusCfdi import StatusCfdi

class TestStatusCfdi(unittest.TestCase):
    urlProd = config.URL_SAT
    soapAction = config.SOAP_ACTION
    rfcEmisor = config.RFC_EMISOR_SAT
    rfcReceptor = config.RFC_RECEPTOR_SAT
    total = config.TOTAL_SAT
    uuidCfdi = config.UUID_SAT
    uuidNotFound = config.ID_NOT_FOUND

    def testStatusCfdi(self):
        objStatus = StatusCfdi.status(self.rfcEmisor, self.rfcReceptor, self.total, self.uuidCfdi,
                                      self.urlProd, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.status_code_sat)
        self.assertIsNotNone(objStatus.is_cancelable)
        self.assertIsNotNone(objStatus.state)
        #El SAT manda EstatusCancelacion vacío mientras el comprobante sigue vigente, de
        #modo que la prueba afirma que el campo se expone, no que traiga valor.
        self.assertTrue(hasattr(objStatus, "cancelation_status"))

    def testStatusCfdi_notFound(self):
        #Un UUID que no existe responde igual con 200, con el código de estatus del SAT.
        objStatus = StatusCfdi.status(self.rfcEmisor, self.rfcReceptor, self.total, self.uuidNotFound,
                                      self.urlProd, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.status_code_sat)

    def testStatusCfdi_totalDistinto(self):
        objStatus = StatusCfdi.status(self.rfcEmisor, self.rfcReceptor, "1.00", self.uuidCfdi,
                                      self.urlProd, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.status_code_sat)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatusCfdi)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
