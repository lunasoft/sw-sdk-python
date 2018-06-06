import json
import base64
from idlelib.iomenu import encoding
import unittest
from SWSDKPython import SWSDKPython


class Samples(unittest.TestCase):
    url = "http://services.test.sw.com.mx"
    user = "demo"
    passwrd = "123456789"

    def get_token(self):
        swservice: SWSDKPython = SWSDKPython()
        resultToken = swservice.authenticate(self.url, self.user, self.passwrd)
        token = json.loads(resultToken)
        return token['data']['token']

    def get_xml(self):
        with open("basico.xml", "rb") as xml:
            encoded_string = base64.b64encode(xml.read())
        return str(encoded_string, encoding)

    def test_getToken(self):
        swservice: SWSDKPython = SWSDKPython()
        resultToken = swservice.authenticate(self.url, self.user, self.passwrd)
        token = json.loads(resultToken)
        self.assertEqual(token['status'], 'success')

    def test_stamp_v4_ok(self):
        swservice: SWSDKPython = SWSDKPython()
        stamp = swservice.stamp(self.url, self.get_token(), self.get_xml(), "v4", True)
        result = json.loads(stamp)
        self.assertEqual(result['message'], '307. El comprobante contiene un timbre previo.')

    def test_account_balance(self):
        swservice: SWSDKPython = SWSDKPython()
        accBalance = swservice.account_balance(self.url, self.get_token())
        acBaIdCliente = json.loads(accBalance)
        self.assertEqual(acBaIdCliente['data']['idSaldoCliente'], '126eac70-425d-4493-87af-93505bfca746')

    def test_validate_lrfc(self):
        swservice: SWSDKPython = SWSDKPython()
        valida_lrfc = json.loads(swservice.validate_lrfc(self.url, self.get_token(), 'LAN7008173R5'))
        self.assertEqual(valida_lrfc['data']['contribuyenteRFC'], 'LAN7008173R5')

    def test_validate_lco(self):
        swservice: SWSDKPython = SWSDKPython()
        validate_lco = json.loads(swservice.validate_lco(self.url, self.get_token(), '20001000000300022816'))
        self.assertEqual(validate_lco['data']['rfc'], 'LAN8507268IA')

    def test_validate_xml(self):
        swservice: SWSDKPython = SWSDKPython()
        validate_xml = json.loads(swservice.validate(self.url, self.get_token(), self.get_xml(), True))
        self.assertEqual(validate_xml['message'], 'Invalid length for a Base-64 char array or string.')

if __name__ == '__main__':
    unittest.main()

