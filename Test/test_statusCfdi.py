import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from Test.base import SdkTestCase
from StatusCfdi.StatusCfdi import StatusCfdi

class TestStatusCfdi(SdkTestCase):
    urlSat = config.URL_SAT
    soapAction = config.SOAP_ACTION
    uuidNotFound = config.ID_NOT_FOUND
    totalDistinto = "1.00"

    #La consulta no lleva credenciales, pero el comprobante se busca en la cuenta.
    requeridas = ("SDKTEST_TOKEN",)

    @classmethod
    def expresion(cls, cancelado=False):
        #Los cuatro datos de la expresión impresa salen de un comprobante de la propia
        #cuenta, nunca de uno ajeno fijado a mano.
        registro = cls.stamped_cfdi(cancelado)
        return (registro["emisorRfc"], registro["receptorRfc"],
                str(registro["total"]), registro["uuid"])

    #UT Consulta estatus
    def testStatusCfdi(self):
        rfcEmisor, rfcReceptor, total, uuid = self.expresion()
        objStatus = StatusCfdi.status(rfcEmisor, rfcReceptor, total, uuid,
                                      self.urlSat, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.status_code_sat)
        self.assertEqual("Vigente", objStatus.state)
        self.assertIsNotNone(objStatus.is_cancelable)
        #EstatusCancelacion viene vacío incluso cuando el comprobante está cancelado, de
        #modo que la prueba afirma que el campo se expone, no que traiga valor.
        self.assertTrue(hasattr(objStatus, "cancelation_status"))

    def testStatusCfdi_cancelado(self):
        rfcEmisor, rfcReceptor, total, uuid = self.expresion(True)
        objStatus = StatusCfdi.status(rfcEmisor, rfcReceptor, total, uuid,
                                      self.urlSat, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertEqual("Cancelado", objStatus.state)

    def testStatusCfdi_notFound(self):
        #Un UUID que no existe responde igual con 200, con el código de estatus del SAT.
        rfcEmisor, rfcReceptor, total, _ = self.expresion()
        objStatus = StatusCfdi.status(rfcEmisor, rfcReceptor, total, self.uuidNotFound,
                                      self.urlSat, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIn("602", objStatus.status_code_sat)

    def testStatusCfdi_totalDistinto(self):
        #El total forma parte de la expresión impresa: si no coincide, el comprobante no
        #se resuelve aunque el UUID exista.
        rfcEmisor, rfcReceptor, _, uuid = self.expresion()
        objStatus = StatusCfdi.status(rfcEmisor, rfcReceptor, self.totalDistinto, uuid,
                                      self.urlSat, self.soapAction)
        self.assertTrue(objStatus.status_code == 200)
        self.assertIn("601", objStatus.status_code_sat)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatusCfdi)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
