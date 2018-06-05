from array import array
import json
import base64
from idlelib.iomenu import encoding
import unittest
from SWSDKPython import SWSDKPython

class Samples(unittest.TestCase):

    url = "http://services.test.sw.com.mx"
    user = "demo"
    passwrd = "123456789"

    def test_getToken(self):
        swservice: SWSDKPython = SWSDKPython()
        resultToken = swservice.authenticate(self.url, self.user, self.passwrd)
        token = json.loads(resultToken)
        self.assertEqual(token['status'], 'success')

    def test_stamp_v4_ok(self):
        with open("basico.xml", "rb") as xml:
            encoded_string = base64.b64encode(xml.read())
        swservice: SWSDKPython = SWSDKPython()
        resultToken = swservice.authenticate(self.url, self.user, self.passwrd)
        token = json.loads(resultToken)
        stamp = swservice.stamp(self.url, token['data']['token'], str(encoded_string, encoding), "v4", True)
        result = json.loads(stamp)
        self.assertEqual(result['message'], '307. El comprobante contiene un timbre previo.')

    def test_account_balance(self):
        swservice: SWSDKPython = SWSDKPython()
        resultToken = swservice.authenticate(self.url, self.user, self.passwrd)
        token = json.loads(resultToken)
        accBalance = swservice.accountBalance(self.url, token['data']['token'])
        acBaIdCliente = json.loads(accBalance)
        self.assertEqual(acBaIdCliente['data']['idSaldoCliente'], '126eac70-425d-4493-87af-93505bfca746')

    def test_valida_lrfc(self):
        



if __name__ == '__main__':
    unittest.main()