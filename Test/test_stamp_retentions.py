import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Test import config
from Test.base import SdkTestCase
from Stamp_Retentions.Stamp_Retentions import Stamp_Retentions


class TestStampRetentions(SdkTestCase):
    codeStamped = config.CODE_STAMPED
    codeExpired = config.CODE_EXPIRED

    #UT Timbrado de retenciones
    def testStampRetentions_xml(self):
        """Prueba timbrado con XML usando token"""
        
        stamp = Stamp_Retentions(self.url, self.token)
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retentions_v3(xml_content)
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
        response = stamp.stamp_retentions_v3(xml_content)
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
        response = stamp.stamp_retentions_v3(xml_content)
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
        response = stamp.stamp_retentions_v3(xml_content)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def testStampRetentions_invalidToken(self):
        """Prueba error con un token invalido"""
        stamp = Stamp_Retentions(self.url, "token-invalido")
        xml_content = TestStampRetentions.open_file("Test/resources/retenciones20.xml")
        response = stamp.stamp_retentions_v3(xml_content)
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStampRetentions)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())


