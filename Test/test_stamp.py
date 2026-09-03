import unittest
import os
import sys
from base64 import b64encode

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from Stamp.Stamp import Stamp

class TestStamp(unittest.TestCase):
    expected = "success"
    expectedError = "error"
    url = "https://services.test.sw.com.mx"
    #xml40Stamp.xml viene sellado y timbrado, y el servicio valida el sello, de modo
    #que la suite no puede reemitirlo: el resultado esperado es el timbre previo.
    codeStamped = "307"

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

    #UT Timbrado
    def testStamp_auth(self):
        stamp = Stamp(self.url, None, self.user, self.password)
        response = stamp.stamp_v4(TestStamp.open_file("Test/resources/xml40Stamp.xml"))
        if response.get_status() == self.expectedError:
            self.assertIn(self.codeStamped, response.get_message())
        else:
            self.assertEqual(self.expected, response.get_status())
            self.assertIsNotNone(response.get_data())

    def testStamp(self):
        stamp = Stamp(self.url, self.token)
        response = stamp.stamp_v4(TestStamp.open_file("Test/resources/xml40Stamp.xml"))
        if response.get_status() == self.expectedError:
            self.assertIn(self.codeStamped, response.get_message())
        else:
            self.assertEqual(self.expected, response.get_status())
            self.assertIsNotNone(response.get_data())

    def testStamp_b64(self):
        #El servicio también acepta el XML en base 64.
        stamp = Stamp(self.url, self.token)
        xml = TestStamp.open_file("Test/resources/xml40Stamp.xml")
        response = stamp.stamp_v4(b64encode(xml.encode("utf-8")).decode("utf-8"), True)
        if response.get_status() == self.expectedError:
            self.assertIn(self.codeStamped, response.get_message())
        else:
            self.assertEqual(self.expected, response.get_status())

    #UT de Error
    def testStamp_invalidXml(self):
        stamp = Stamp(self.url, self.token)
        response = stamp.stamp_v4("<xml>no es un cfdi</xml>")
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

    def testStamp_invalidToken(self):
        stamp = Stamp(self.url, "token-invalido")
        response = stamp.stamp_v4(TestStamp.open_file("Test/resources/xml40Stamp.xml"))
        self.assertEqual(self.expectedError, response.get_status())
        self.assertIsNotNone(response.get_message())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStamp)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
