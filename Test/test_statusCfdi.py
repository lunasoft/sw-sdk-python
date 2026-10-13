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
    uuidNotFound = config.ID_NOT_FOUND
    uuidInvalid = config.ID_INVALID
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
        objStatus = StatusCfdi(self.urlSat).status(rfcEmisor, rfcReceptor, total, uuid)
        self.assertTrue(self.expected == objStatus.get_status())
        self.assertTrue(objStatus.status_code == 200)
        self.assertIsNotNone(objStatus.status_code_sat)
        self.assertEqual("Vigente", objStatus.state)
        self.assertIsNotNone(objStatus.is_cancelable)
        #EstatusCancelacion llega con i:nil="true" incluso cuando el comprobante está
        #cancelado, y se expone como None.
        self.assertIsNone(objStatus.cancelation_status)

    def testStatusCfdi_cancelado(self):
        rfcEmisor, rfcReceptor, total, uuid = self.expresion(True)
        objStatus = StatusCfdi(self.urlSat).status(rfcEmisor, rfcReceptor, total, uuid)
        self.assertTrue(self.expected == objStatus.get_status())
        self.assertEqual("Cancelado", objStatus.state)

    def testStatusCfdi_notFound(self):
        #Un UUID que no existe responde igual con 200, con el código de estatus del SAT.
        rfcEmisor, rfcReceptor, total, _ = self.expresion()
        objStatus = StatusCfdi(self.urlSat).status(rfcEmisor, rfcReceptor, total, self.uuidNotFound)
        self.assertTrue(self.expected == objStatus.get_status())
        self.assertIn("602", objStatus.status_code_sat)

    def testStatusCfdi_totalDistinto(self):
        #El total forma parte de la expresión impresa: si no coincide, el comprobante no
        #se resuelve aunque el UUID exista.
        rfcEmisor, rfcReceptor, _, uuid = self.expresion()
        objStatus = StatusCfdi(self.urlSat).status(rfcEmisor, rfcReceptor, self.totalDistinto, uuid)
        self.assertTrue(self.expected == objStatus.get_status())
        self.assertIn("601", objStatus.status_code_sat)

    #UT de Error
    def testStatusCfdi_invalidUuid(self):
        #El ambiente de pruebas responde un UUID mal formado con un SOAP Fault y HTTP 500;
        #producción responde 200 con el código 602.
        rfcEmisor, rfcReceptor, total, _ = self.expresion()
        objStatus = StatusCfdi(self.urlSat).status(rfcEmisor, rfcReceptor, total, self.uuidInvalid)
        self.assertTrue(self.expectedError == objStatus.get_status())
        self.assertTrue(500 == objStatus.get_status_code())
        self.assertIn("Guid", objStatus.get_message_detail())

    #UT de Configuración
    def testStatusCfdi_withoutUrl(self):
        with self.assertRaises(ValueError):
            StatusCfdi("")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatusCfdi)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
