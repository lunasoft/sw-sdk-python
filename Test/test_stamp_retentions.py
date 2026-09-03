import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Stamp_Retentions.Stamp_Retentions import Stamp_Retentions


class TestStampRetentions(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    #retenciones20.xml viene sellado con su FechaExp, y el servicio valida el sello,
    #de modo que la suite no puede refrescar la fecha: el servicio contesta 307 si la
    #retención ya se timbró, o 401 cuando la fecha del fixture rebasa las 72 horas.
    codeStamped = "307"
    codeExpired = "401"

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

    #UT de Timbrado de retenciones
    def testStampRetentions_xml(self):
        """Prueba timbrado con XML usando token"""
        
        stamp = Stamp_Retentions(self.url, self.token)
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        if response.get_status() == self.expectedError:
            self.assertTrue(self.codeStamped in response.get_message() or self.codeExpired in response.get_message())
        else:
            self.assertEqual(self.expected, response.get_status())
            self.assertIsNotNone(response.get_data())

    def testStampRetentions_auth(self):
        """Prueba timbrado con autenticación de cuenta"""
        
        stamp = Stamp_Retentions(
            self.url,
            None,
            self.user,
            self.password
        )
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        if response.get_status() == self.expectedError:
            self.assertTrue(self.codeStamped in response.get_message() or self.codeExpired in response.get_message())
        else:
            self.assertEqual(self.expected, response.get_status())
            self.assertIsNotNone(response.get_data())

    #UT de Error
    def testStampRetentions_xml_Error(self):
        """Prueba error timbrado con XML CFDI"""

        stamp = Stamp_Retentions(self.url, self.token)
        xml_content = TestStampRetentions.open_file("Test/resources/xml40.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def testStampRetentions_authError(self):
        """Prueba error timbrado con autenticación de cuenta"""
        
        stamp = Stamp_Retentions(
            self.url,
            None,
            "wrongUser",
            self.password
        )
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def testStampRetentions_invalidToken(self):
        """Prueba error con un token invalido"""
        stamp = Stamp_Retentions(self.url, "token-invalido")
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retetions_v3(xml_content)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStampRetentions)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())


