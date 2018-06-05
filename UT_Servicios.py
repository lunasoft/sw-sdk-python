import SWSDKPython
import json
import base64
from idlelib.iomenu import encoding

# Prueba
url = "http://services.test.sw.com.mx"
user = "demo"
passwrd = "123456789"

with open("basico.xml", "rb") as xml:
    encoded_string = base64.b64encode(xml.read())


swservice = SWSDKPython.SWSDKPython()
token = json.loads(swservice.authenticate(url, user, passwrd))
print(token['data']['token'])
rToken = token['data']['token']

timbrar = swservice.stamp(url, rToken, str(encoded_string, encoding), "v4", True)
print(timbrar)
accBalance = swservice.accountBalance(url, token['data']['token'])

print("Estado de cuenta "+accBalance)

