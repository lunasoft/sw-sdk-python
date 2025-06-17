# Python

[![SW sapien](https://dka575ofm4ao0.cloudfront.net/pages-transactional_logos/retina/68712/SW_smarter-Servicios_web.png)](http://sw.com.mx/)

Librería *Python* para el consumo de los servicios de SW sapien®.

## Contenido 

- [Compatibilidad](#Compatibilidad)
- [Dependencias](#Dependencias)
- [Documentación](#Documentación)
- [Instalación](#Instalación)
- [Implementación](#Implementación)
---

### Compatibilidad :clipboard:
- CFDI 4.0
- Python 3 o superior

### Dependencias :toolbox:
- **Python 3** o superior.
- [Requests](http://docs.python-requests.org)

### Documentación :open_file_folder:
* [Inicio Rápido](https://developers.sw.com.mx/knowledge-base/conoce-el-proceso-de-integracion-en-solo-7-pasos/)
* [Documentacion Oficial Servicios](http://developers.sw.com.mx)


### Instalación :hammer_and_wrench:

Ejecutar los comandos directamente en la consola tal cual aparecen en la página de la librería requerida, por ejemplo

 ```py
pip install requests
```

### Implementación :gear:

La librería contara con los servicios principales como lo son Timbrado de CFDI, Cancelación, Consulta estatus CFDI, etc.


## Autenticaci&oacute;n ##
El servicio de Autenticación es utilizado para obtener el **token** el cual sera utilizado para consumir los servicios, para poder utilizar este servicio es necesario un **usuario** y **contraseña**.

:pushpin: ***NOTA:*** La clase de authentication, nos sirve para obtener un token de 2 hrs de duración. :hourglass:

Parámetros necesarios: 
- Url Servicios SW
- Usuario y contraseña

**Ejemplo de consumo de la librería para obtener token**
 ```py
objAuth = Auth("http://services.test.sw.com.mx", None, "user", "password")
objResponseAuth = objAuth.authentication()

if objResponseAuth.get_status() == "error":
   print(objResponseAuth.get_status_code())
   print("\nMessage: "+ objResponseAuth.get_message())
   print(objResponseAuth.get_messageDetail())
else:
   print(objResponseAuth.get_status_code())
   print("\nToken: "+objResponseAuth.get_token())
   print(objResponseAuth.get_time_expire())
```

## Timbrado ##

<details>
<summary>
Timbrado CFDI V1
</summary>

**TimbrarV1** Recibe el contenido de un **XML** ya emitido (sellado) en formato **String**  ó tambien puede ser en **Base64**, posteriormente si la factura y el token son correctos devuelve el complemento timbre en un string (**TFD**), en caso contrario lanza una excepción.

Este método recibe los siguientes parametros:
* Archivo en formato **String** ó **Base64**
* Usuario y contraseña ó Token
* Url Servicios SW

:pushpin: ***NOTA:*** **b64** es un parámetro opcional y se debe indicar en *true* si el XML va encodeado en base 64. De no indicarse por defecto se tomará el valor de *false*

**Ejemplo de consumo de la libreria para timbrar XML en formato string utilizando usuario y contraseña**
```py
from Stamp.Stamp import Stamp

#Creamos funcion para abrir nuestro archivo
xml = open("prueba.xml", "r", encoding='ansi', errors='ignore').read()
#Creamos instancia y pasamos parametros
stamp = Stamp("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
response = stamp.stamp_v1(xml)

print(response.get_data())
```

**Ejemplo de consumo de la libreria para timbrar XML en formato string utilizando token** [¿Como obtener token?](http://developers.sw.com.mx/knowledge-base/generar-un-token-infinito/)
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Stamp.Stamp import Stamp

#Creamos funcion para abrir nuestro archivo
xml = open("prueba.xml", "r", encoding='ansi', errors='ignore').read()
#Creamos instancia y pasamos parametros
stamp = Stamp("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
response = stamp.stamp_v1(xml)

if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Ejemplo de consumo de la libreria para timbrar XML en Base64 utilizando token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Stamp.Stamp import Stamp

#Creamos funcion para abrir nuestro archivo
xml = open("prueba.xml", "r", encoding='ansi', errors='ignore').read()
encoded = base64.b64encode(xml.encode('utf-8'))
#Creamos instancia y pasamos parametros
stamp = Stamp("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response = stamp.stamp_v1(encoded.decode(),True)
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Funciones disponibles**
- stamp_v1(xml, b64)
- stamp_v2(xml, b64)
- stamp_v3(xml, b64)
- stamp_v4(xml, b64)
</details>


<details>
<summary>
Emisión Timbrado V1
</summary>

**Emisión Timbrado** Realiza el sellado y timbrado de un comprobante CFDI 3.3 ó CFDI 4.0. Recibe el contenido de un **XML** en formato **String**  ó tambien puede ser en **Base64**, posteriormente si la factura y el token son correctos devuelve el complemento timbre en un string (**TFD**), en caso contrario lanza una excepción.

Este método recibe los siguientes parametros:
* Archivo en formato **String** ó **Base64**
* Usuario y contraseña ó Token
* Url Servicios SW

:pushpin: ***NOTA:*** **b64** es un parámetro opcional y se debe indicar en *true* si el XML va encodeado en base 64. De no indicarse por defecto se tomará el valor de *false*

**Ejemplo de consumo de la libreria para la emisión Timbrado XML en formato string utilizando usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Issue.Issue import Issue

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
#Creamos instancia y pasamos parametros
issue = Issue("http://services.test.sw.com.mx", None, "user", "password")
response = issue.issue_v1(xml)
if response.status ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Ejemplo de consumo de la libreria para la emisión Timbrado XML en formato string utilizando token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Issue.Issue import Issue

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
issue = Issue("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response = issue.issue_v1(xml)
if response.status ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Ejemplo de consumo de la libreria para timbrar XML en Base64 utilizando token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Issue.Issue import Issue

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
encoded = base64.b64encode(xml.encode('utf-8'))
#Creamos instancia y pasamos parametros
issue = Issue("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response = issue.issue_v1(encoded.decode(), True)
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Funciones disponibles**
- issue_v1(xml, b64)
- issue_v2(xml, b64)
- issue_v3(xml, b64)
- issue_v4(xml, b64)

</details>

<details>
<summary>
Emisión Timbrado JSON V1
</summary>

**Emisión Timbrado JSON** Realiza el sellado y timbrado de un comprobante CFDI 3.3 ó CFDI 4.0. Recibe el contenido de un **JSON** en formato **String**, posteriormente si la factura y el token son correctos devuelve el complemento timbre en un string (**TFD**), en caso contrario lanza una excepción

Este método recibe los siguientes parametros:
* Archivo en formato **String**
* Usuario y contraseña ó Token
* Url Servicios SW

**Ejemplo de consumo de la libreria para la emisión Timbrado JSON en formato string utilizando usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Issue.Issue import Issue

#creamos funcion para abrir nuestro archivo
json = open_file("file.json")
issue = Issue("http://services.test.sw.com.mx", None, "user", "password")
response = issue.issue_json_v1(json)
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```
**Ejemplo de consumo de la libreria para la emisión Timbrado JSON en formato string utilizando token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Issue.Issue import Issue

#creamos funcion para abrir nuestro archivo
json = open_file("file.json")
issue = Issue("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
response = issue.issue_json_v1(json)
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Funciones disponibles**
- issue_json_v1(json)
- issue_json_v2(json)
- issue_json_v3(json)
- issue_json_v4(json)


</details>

:pushpin: ***NOTA:*** Existen varias versiones de respuesta, las cuales son las siguientes:

| Version |                         Respuesta                             | 
|---------|---------------------------------------------------------------|
|  V1     | Devuelve el timbre fiscal digital                             | 
|  V2     | Devuelve el timbre fiscal digital y el CFDI timbrado          | 
|  V3     | Devuelve el CFDI timbrado                                     | 
|  V4     | Devuelve todos los datos del timbrado                         |

Para mayor referencia de estas versiones de respuesta, favor de visitar el siguiente [link](https://developers.sw.com.mx/knowledge-base/versiones-de-respuesta-timbrado/).

## Cancelación ##

Este servicio se utiliza para cancelar documentos xml y se puede hacer mediante varios metodos **Cancelación CSD**, **Cancelación PFX**, **Cancelacion por XML** y **Cancelación UUID**.

<details>
<summary>
Cancelacion por CSD
</summary>

Como su nombre lo indica, este método realiza la cancelacion mediante los CSD.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña o token
* UUID
* RFC emisor
* Certificado (.cer)
* Key (.key)
* Password del archivo key
* Motivo
* Folio Sustitución (Si el motivo es 01)

**Ejemplo de consumo de la libreria para cancelar con CSD con motivo de cancelación 02 sin relación a documento mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

#Datos
uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "02"
foliosustitucion = ""
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelCSD = objCancel.CancelCsd(uuid, rfc, b64cert, b64key, cPassword, motivo, foliosustitucion)

if objResponseCancelCSD.get_status() ==  "error":
	print(objResponseCancelCSD.get_message())
	print(objResponseCancelCSD.get_messageDetail())
else:
	print(objResponseCancelCSD.get_data())
```

**Ejemplo de consumo de la libreria para cancelar con CSD con motivo de cancelación 01 con relación a documento mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "01"
foliosustitucion = "01724196-ac5a-4735-b621-e3b42bcbb459"
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelCSD = objCancel.CancelCsd(uuid, rfc, b64cert, b64key, cPassword, motivo, foliosustitucion)

if objResponseCancelCSD.get_status() ==  "error":
	print(objResponseCancelCSD.get_message())
	print(objResponseCancelCSD.get_messageDetail())
else:
	print(objResponseCancelCSD.get_data())
```

</details>

<details>
<summary>
Cancelacion por PFX
</summary>

Como su nombre lo indica, este método realiza la cancelacion mediante el PFX.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña o token
* UUID
* RFC emisor
* Archivo PFX 
* Password (CSD)
* Motivo
* Folio Sustitución

**Ejemplo de consumo de la libreria para cancelar con PFX con motivo de cancelación 02 sin relación a documento mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "02"
foliosustitucion = ""
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelPfx = objCancel.CancelPfx(uuid, rfc, b64Pfx, cPassword, motivo, foliosustitucion)

if objResponseCancelPfx .get_status() ==  "error":
	print(objResponseCancelPfx.get_message())
	print(objResponseCancelPfx.get_messageDetail())
else:
	print(objResponseCancelPfx.get_data())
```

**Ejemplo de consumo de la libreria para cancelar con PFX con motivo 01 con documento relacionado mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "02"
foliosustitucion = "01724196-ac5a-4735-b621-e3b42bcbb459"
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelPfx = objCancel.CancelPfx(uuid, rfc, b64Pfx, cPassword, motivo, foliosustitucion)

if objResponseCancelPfx.get_status() ==  "error":
	print(objResponseCancelPfx.get_message())
	print(objResponseCancelPfx.get_messageDetail())
else:
	print(objResponseCancelPfx.get_data())
```
</details>

<details>
<summary>
Cancelacion por XML
</summary>

Como su nombre lo indica, este método realiza la cancelacion mediante el XML sellado con los UUID a cancelar.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña o token
* XML sellado con los UUID a cancelar.

**Ejemplo de XML para Cancelar**
```xml
<Cancelacion xmlns="http://cancelacfd.sat.gob.mx"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" Fecha="2021-12-26T18:15:28" RfcEmisor="EKU9003173C9">
    <Folios>
        <Folio UUID="fe4e71b0-8959-4fb9-8091-f5ac4fb0fef8" Motivo="02" FolioSustitucion=""/>
    </Folios>
    <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        <SignedInfo>
            <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" />
            <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" />
            <Reference URI="">
                <Transforms>
                    <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" />
                </Transforms>
                <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" />
                <DigestValue>XEdUtCptjdlz9DsYAP7nnU6MytU=</DigestValue>
            </Reference>
        </SignedInfo>
        <SignatureValue>ZnWh91e5tUc4/t1ZWnb3yOgB8zuCXNPioND+rv6aLOEwIw26/8sYYb+GT4wgyqlc09wOs32XTUwWoGQwtWMG8Euqq+4xJyobWvPCsX6CiURvD/Pd33xgkH92A0AGQxEMYGVT7wK+GFS2gDTYEYAXvZqzCe6+rXnlQvHML0TOOmhVu/wc8YrCbGt4z/F5sRxhjpa0eqwFEq4RmB4nkWjcD3Pnudn3XAI5NHIiOd8KVGVcDR+LvYvKj7h+18WxZgujpggYjbFN79i1jEsAEPDfgryUdTvjDw+KC7Mg+/ge6pssH42buEMIwVE4VX9Y3NtWSGTwdIK/8pxXk+Y5wyR6Gg==</SignatureValue>
        <KeyInfo>
            <X509Data>
                <X509IssuerSerial>
                    <X509IssuerName>OID.1.2.840.113549.1.9.2=responsable: ACDMA-SAT, OID.2.5.4.45=2.5.4.45, L=COYOACAN, S=CIUDAD DE MEXICO, C=MX, PostalCode=06370, STREET=3ra cerrada de cadiz, E=oscar.martinez@sat.gob.mx, OU=SAT-IES Authority, O=SERVICIO DE ADMINISTRACION TRIBUTARIA, CN=AC UAT</X509IssuerName>
                    <X509SerialNumber>292233162870206001759766198444326234574038512436</X509SerialNumber>
                </X509IssuerSerial>
                <X509Certificate>MIIFuzCCA6OgAwIBAgIUMzAwMDEwMDAwMDA0MDAwMDI0MzQwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWRpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMTkwNjE3MTk0NDE0WhcNMjMwNjE3MTk0NDE0WjCB4jEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gWElRQjg5MTExNlFFNDEeMBwGA1UEBRMVIC8gWElRQjg5MTExNk1HUk1aUjA1MR4wHAYDVQQLExVFc2N1ZWxhIEtlbXBlciBVcmdhdGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCN0peKpgfOL75iYRv1fqq+oVYsLPVUR/GibYmGKc9InHFy5lYF6OTYjnIIvmkOdRobbGlCUxORX/tLsl8Ya9gm6Yo7hHnODRBIDup3GISFzB/96R9K/MzYQOcscMIoBDARaycnLvy7FlMvO7/rlVnsSARxZRO8Kz8Zkksj2zpeYpjZIya/369+oGqQk1cTRkHo59JvJ4Tfbk/3iIyf4H/Ini9nBe9cYWo0MnKob7DDt/vsdi5tA8mMtA953LapNyCZIDCRQQlUGNgDqY9/8F5mUvVgkcczsIgGdvf9vMQPSf3jjCiKj7j6ucxl1+FwJWmbvgNmiaUR/0q4m2rm78lFAgMBAAGjHTAbMAwGA1UdEwEB/wQCMAAwCwYDVR0PBAQDAgbAMA0GCSqGSIb3DQEBCwUAA4ICAQBcpj1TjT4jiinIujIdAlFzE6kRwYJCnDG08zSp4kSnShjxADGEXH2chehKMV0FY7c4njA5eDGdA/G2OCTPvF5rpeCZP5Dw504RZkYDl2suRz+wa1sNBVpbnBJEK0fQcN3IftBwsgNFdFhUtCyw3lus1SSJbPxjLHS6FcZZ51YSeIfcNXOAuTqdimusaXq15GrSrCOkM6n2jfj2sMJYM2HXaXJ6rGTEgYmhYdwxWtil6RfZB+fGQ/H9I9WLnl4KTZUS6C9+NLHh4FPDhSk19fpS2S/56aqgFoGAkXAYt9Fy5ECaPcULIfJ1DEbsXKyRdCv3JY89+0MNkOdaDnsemS2o5Gl08zI4iYtt3L40gAZ60NPh31kVLnYNsmvfNxYyKp+AeJtDHyW9w7ftM0Hoi+BuRmcAQSKFV3pk8j51la+jrRBrAUv8blbRcQ5BiZUwJzHFEKIwTsRGoRyEx96sNnB03n6GTwjIGz92SmLdNl95r9rkvp+2m4S6q1lPuXaFg7DGBrXWC8iyqeWE2iobdwIIuXPTMVqQb12m1dAkJVRO5NdHnP/MpqOvOgLqoZBNHGyBg4Gqm4sCJHCxA1c8Elfa2RQTCk0tAzllL4vOnI1GHkGJn65xokGsaU4B4D36xh7eWrfj4/pgWHmtoDAYa8wzSwo2GVCZOs+mtEgOQB91/g==</X509Certificate>
            </X509Data>
        </KeyInfo>
    </Signature>
</Cancelacion>
```
Para caso de motivo 01 deberá añadir el atributo "FolioSustitucion" dentro del Nodo <Folio>

Ejemplo de nodo Folio: 
```
<Folios>
	<Folio UUID="b374db50-a0a3-4028-9d01-32b93e2b925a" Motivo="01" FolioSustitucion="b3641a4b-7177-4323-aaa0-29bd34bf1ff8" />
</Folios>
```

**Ejemplo de consumo de la libreria para cancelar con XML mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

#Creamos funcion para abrir nuestro archivo
xmlCancel = open_file("file.xml")
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelXml  = objCancel.CancelXml(xmlCancel)

if objResponseCancelXml.get_status() ==  "error":
	print(objResponseCancelXml.get_message())
	print(objResponseCancelXml.get_messageDetail())
else:
	print(objResponseCancelXml.get_data())
```
</details>

<details>
<summary>
Cancelacion por UUID
</summary>

Como su nombre lo indica, este método realiza la cancelacion mediante el UUID a cancelar.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña o token
* RFC emisor
* UUID
* Motivo
* Folio Sustitución

**Ejemplo de consumo de la libreria para cancelar con UUID con motivo de cancelación 02 sin documento relacionado mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

#Datos
uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "02"
foliosustitucion = ""
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelUuid = objCancel.CancelUuid(uuid, rfc, motivo, foliosustitucion)

if objResponseCancelUuid.get_status() ==  "error":
	print(objResponseCancelUuid.get_message())
	print(objResponseCancelUuid.get_messageDetail())
else:
	print(objResponseCancelUuid.get_data())
```

**Ejemplo de consumo de la libreria para cancelar con UUID con motivo de cancelación 01 con documento relacionado mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

#Datos
uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "01"
foliosustitucion = "01724196-ac5a-4735-b621-e3b42bcbb459"
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelUuid = objCancel.CancelUuid(uuid, rfc, motivo, foliosustitucion)

if objResponseCancelUuid.get_status() ==  "error":
	print(objResponseCancelUuid.get_message())
	print(objResponseCancelUuid.get_messageDetail())
else:
	print(objResponseCancelUuid.get_data())
```
</details>

## Usuarios V2 ##
Métodos para realizar la consulta de informacion de usuarios, así como la creación, actualización y eliminacion  de los mismos

> [!IMPORTANT]
> Los métodos han tenido algunos cambios y mejoras con respecto a la versión 1.

<details>
  <summary>Crear usuario</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* Informacion del nuevo cliente

***Información del cliente:*** 

| Dato              | Descripción                                  |
|-------------------|----------------------------------------------|
| name              | Nombre del usuario                           |
| taxId             | RFC del usuario                              |
| email             | correo del nuevo usuario                     |
| stamps            | Cantidad de timbres a asignar                |
| isUnlimited       | Especificar si tendra timbres ilimitados     |
| password          | Contraseña del usuario                       |
| notificationEmail | Correo a donde quiere recibir notificaciones |
| phone             | Número del telefono del usuario              |

**Ejemplo de consumo de la libreria para crear un usuario mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
name = "Prueba UT Hijo Python"
taxId = "XAXX010101000"
email = "usuario_prueba@example.com"
stamps = 1
isUnlimited = False
password = "_123456789"
notificationEmail = "usuario_prueba@example.com"
phone = "0000000000"
objResponseAccountUser = objAccountUser.create_user(name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Procesamiento de la respuesta
	for Key,Value in objResponseAccountUser.response["data"].items():
  		print (Key,"=",Value)
```

**Ejemplo de consumo de la libreria para crear un usuario mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
name = "Prueba UT Hijo Python"
taxId = "XAXX010101000"
email = "usuario_prueba@example.com"
stamps = 1
isUnlimited = False
password = "_123456789"
notificationEmail = "usuario_prueba@example.com"
phone = "0000000000"
objResponseAccountUser = objAccountUser.create_user(name,taxId,email,stamps,isUnlimited,password,notificationEmail,phone)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Procesamiento de la respuesta
	for Key,Value in objResponseAccountUser.response["data"].items():
  		print (Key,"=",Value)
```

:pushpin: ***NOTA:*** La contraseña debe cumplir con las siguientes politicas:
* La contraseña no debe ser igual que el nombre de usuario.
* La contraseña debe incluir al menos una letra mayúscula.
* La contraseña debe incluir al menos una letra minúscula
* La contraseña debe incluir al menos un número.
* La contraseña debe incluir al menos un símbolo (carácter especial).
* La contraseña no debe incluir espacios en blanco.
* La contraseña debe tener entre 10 y 20 caracteres.
* La contraseña no debe incluir símbolos especiales fuera de lo común.
* Los caracteres especiales aceptados son los siguientes: !@#$%^&*()_+=\[{\]};:<>|./?,-]
</details>

<details>
  <summary>Actualizacion de datos de usuario</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* IdUser
* Datos nuevos del cliente

***Información nueva del cliente:*** 

| Dato              | Descripción                              |
|-------------------|------------------------------------------|
| idUser            | Id del usuario a actualizar              |
| name              | Nuevo nombre del usuario                 |
| taxId             | Nuevo RFC del usuario                    |
| notificationEmail | Nuevo correo para recibir notificaciones |
| isUnlimited       | Especificar si tendra timbres ilimitados |
| phone             | Número del telefono del usuario          |



> [!NOTE]  
> Puedes asignarles "None" a las propiedades que no vayas a actualizar.

**Ejemplo de consumo de la libreria para actualizar usuarios**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
idUser = "b9e42c65-4afa-45a2-9b0d-d67b1373a7f4"
name = "Prueba UT Hijo Python Actualizado"
taxId = "XAXX010101002"
notificationEmail = None
phone = "0000000001"
isUnlimited = False
objResponseAccountUser = objAccountUser.update_user(idUser,name,taxId,notificationEmail,phone,isUnlimited)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos como Respuesta el IdUser
	print(objResponseAccountUser.get_data())
```

**Ejemplo de consumo de la libreria para actualizar usuarios mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
idUser = "b9e42c65-4afa-45a2-9b0d-d67b1373a7f4"
name = "Prueba UT Hijo Python Actualizado"
taxId = "XAXX010101002"
notificationEmail = None
phone = "0000000001"
isUnlimited = False
objResponseAccountUser = objAccountUser.update_user(idUser,name,taxId,notificationEmail,phone,isUnlimited)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos como Respuesta el IdUser
	print(objResponseAccountUser.get_data())
```
</details>

<details>
  <summary>Eliminación de usuario</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* IdUser

**Ejemplo de consumo de la libreria para eliminar usuarios**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
idUser = "8e6ec77d-b4d6-47aa-95b9-89b354d8207b"
objResponseAccountUser = objAccountUser.delete_user(idUser)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos como Respuesta el IdUser
	print(objResponseAccountUser.get_data())
```

**Ejemplo de consumo de la libreria para eliminar usuarios mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
idUser = "8e6ec77d-b4d6-47aa-95b9-89b354d8207b"
objResponseAccountUser = objAccountUser.delete_user(idUser)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos como Respuesta el IdUser
	print(objResponseAccountUser.get_data())
```
</details>
<details>
  <summary>Obtener todos los usuarios</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token de la cuenta padre.
* Url Servicios SW
* Url Api

**Ejemplo de consumo de la libreria para obtener todos los usarios de una cuenta administradora o padre**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
objResponseAccountUser = objAccountUser.getUser_all()
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos los datos de los usuarios
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
**Ejemplo de consumo de la libreria para obtener todos los usarios de una cuenta administradora o padre mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
objResponseAccountUser = objAccountUser.getUser_all()
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos los datos de los usuarios
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```

</details>
<details>
  <summary>Obtener usuario por ID</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token de la cuenta padre
* Url Servicios SW
* Url Api
* IdUser

**Ejemplo de consumo de la libreria para obtener usuario por ID**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
idUser = "32501CF2-DC62-4370-B47D-25024C44E131"
objResponseAccountUser = objAccountUser.getUser_by_idUser(idUser)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
**Ejemplo de consumo de la libreria para obtener usuario por ID mediante el token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
idUser = "32501CF2-DC62-4370-B47D-25024C44E131"
objResponseAccountUser = objAccountUser.getUser_by_idUser(idUser)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
</details>
<details>
  <summary>Obtener usuarios por Email</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* Email del usuario a consulta.

**Ejemplo de consumo de la libreria para obtener todos los usuarios**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
email = "usuario_prueba@example.com"
objResponseAccountUser = objAccountUser.getUser_by_email(email)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
**Ejemplo de consumo de la libreria para obtener todos los usuarios mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
email = "usuario_prueba@example.com"
objResponseAccountUser = objAccountUser.getUser_by_email(email)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
</details>
<details>
  <summary>Obtener usuarios por RFC</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* RFC del usuario a consultar.

**Ejemplo de consumo de la libreria para obtener todos los usuarios**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
taxId = "AAAA000101010"
objResponseAccountUser = objAccountUser.getUser_by_taxId(taxId)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
**Ejemplo de consumo de la libreria para obtener todos los usuarios mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
taxId = "AAAA000101010"
objResponseAccountUser = objAccountUser.getUser_by_taxId(taxId)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
</details>
<details>
  <summary>Obtener usuarios que esten activos o desactivados</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* Indica si el Usuario es activo o no (true o false)

**Ejemplo de consumo de la libreria para obtener todos los usuarios**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",None,user,password)
objResponseAccountUser = objAccountUser.getUser_by_isActive(True)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
**Ejemplo de consumo de la libreria para obtener todos los usuarios mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AccountUser.AccountUser import AccountUser

objAccountUser = AccountUser("https://services.test.sw.com.mx","https://api.test.sw.com.mx",token)
objResponseAccountUser = objAccountUser.getUser_by_isActive(True)
#En caso de error, obtenemos el mensaje
if objResponseAccountUser.get_status() ==  "error":
	print(objResponseAccountUser.get_message())
	print(objResponseAccountUser.get_messageDetail())
else:
	#Obtenemos la respuesta
	for user in response.data.items:
        print("\tName: ",user.name)
        print("\tIdDelear: ",user.idDealer)
        print("\tIdUser: ",user.idUser)
        print("\t taxId: ",user.taxId)
        print("\t username: ",user.username)
        print("\t email: ",user.email)
        print("\t profile: ",user.profile)
        print("\t isAcrtive: ",user.isActive)
        print("\t accessToken: ",user.accessToken)
        print("\t stamps: ",user.stamps)
        print("\t phone: ",user.phone)
        print("\t isUnlimited: ",user.isUnlimited)
```
</details>

## Balance (Administración de saldo) ##
Métodos para realizar la consulta de saldo así como la asignación y eliminación de timbres a un usuario.

<details>
  <summary>Consulta de timbres</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api

> [!IMPORTANT]  
> Los nombres de las variables en la respuesta y la petición han cambiado.

**Ejemplo de consumo de la libreria para consultar el saldo mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBalance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, user, password)
objResponseBalance = objBalance.get_balance()
#En caso de error, obtenemos el mensaje
if objResponseBalance.get_status() ==  "error":
	print(objResponseBalance.get_message())
	print(objResponseBalance.get_messageDetail())
else:
	#Obtenemos los datos
	print(objResponseBalance.data.idUser)
	print(objResponseBalance.data.idUserBalance)
    print(objResponseBalance.data.stampsAssigned)
	print(objResponseBalance.data.stampsUsed)
	print(objResponseBalance.data.stampsBalance)
```

**Ejemplo de consumo de la libreria para consultar el saldo mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBalance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", token)
objResponseBalance = objBalance.get_balance()
#En caso de error, obtenemos el mensaje
if objResponseBalance.get_status() ==  "error":
	print(objResponseBalance.get_message())
	print(objResponseBalance.get_messageDetail())
else:
	#Obtenemos los datos
	print(objResponseBalance.data.idUser)
	print(objResponseBalance.data.idUserBalance)
    print(objResponseBalance.data.stampsAssigned)
	print(objResponseBalance.data.stampsUsed)
	print(objResponseBalance.data.stampsBalance)
```
</details>

<details>
  <summary>Agregar timbres</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* IdUser
* Número de timbres
* Comentario

> [!NOTE] 
> El servicio regresa unicamente la cantidad de timbres despues del abono de timbres.

**Ejemplo de consumo de la libreria para agregar timbres  mediante usuario  y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBalance= Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, user, password)
objResponseBalance = objBalance.add_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Asignación de 1 timbre")
#En caso de error, obtenemos el mensaje
if objResponseBalance.get_status() ==  "error":
	print(objResponseBalance.get_message())
	print(objResponseBalance.get_messageDetail())
else:
	#Obtenemos la cantidad de timbres posterior a la asignación
	print(objResponseBalance.get_data())
```
**Ejemplo de consumo de la libreria para agregar timbres  mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBalance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", token)
objResponseBalance = objBalance.add_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Asignación de 1 timbre")
#En caso de error, obtenemos el mensaje
if objResponseBalance.get_status() ==  "error":
	print(objResponseBalance.get_message())
	print(objResponseBalance.get_messageDetail())
else:
	#Obtenemos la cantidad de timbres posterior a la asignación
	print(objResponseBalance.get_data())
```
</details>
<details>
  <summary>Eliminar timbres</summary>

<br>Este método recibe los siguientes parametros:
* Usuario y contraseña o Token
* Url Servicios SW
* Url Api
* IdUser
* Número de timbres
* Comentario

> [!NOTE]
> El servicio regresa unicamente la cantidad de timbres despues de remover los timbres.

**Ejemplo de consumo de la libreria para remover timbres mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBalance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", None, user, password)
objResponseBalance = objBalance.remove_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Remover 1 timbre por falta de pago")
#En caso de error, obtenemos el mensaje
if objResponseBalance.get_status() ==  "error":
	print(objResponseBalance.get_message())
	print(objResponseBalance.get_messageDetail())
else:
	#Obtenemos la cantidad de timbres posterior a remover los timbres
	print(objResponseBalance.get_data())
```

**Ejemplo de consumo de la libreria para remover timbres mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBalance = Balance("https://services.test.sw.com.mx","https://api.test.sw.com.mx", token)
objResponseBalance = objBalance.remove_stamps("32501CF2-DC62-4370-B47D-25024C44E131",1,"Remover 1 timbre por falta de pago")
#En caso de error, obtenemos el mensaje
if objResponseBalance.get_status() ==  "error":
	print(objResponseBalance.get_message())
	print(objResponseBalance.get_messageDetail())
else:
	#Obtenemos la cantidad de timbres posterior a remover los timbres
	print(objResponseBalance.get_data())
```
</details>

## Validación ##

<details>
<summary>
Validación XML
</summary>

Este servicio recibe un comprobante CFDI 3.3 ó 4.0 en formato XML mediante el cual se valida integridad, sello, errores de estructura, matriz de errores del SAT incluyendo complementos, se valida que exista en el SAT, así como el estatus en el SAT.

Este metodo recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña o token
* XML

**Ejemplo de consumo de la libreria para validación de XML mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Validate.Validate import Validate

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
objValidate = Validate("http://services.test.sw.com.mx", , None ,"user","password")
objResponseValidateXml = objValidate.ValidateXml(xml)

#Respuesta
print(objResponseValidateXml.get_response())
#Procesamiento de la respuesta

for d in objResponseValidateXml.response["detail"]:
	print("Detail:")
	for detail in d["detail"]:
		print("\tmessage: ", detail["message"])
		print("\tmessageDetail: ", detail["messageDetail"])
		print("\tType: ", str(detail["type"]))
	print("Section: ", d["section"])
print("\ncadenaOriginalSAT: ",objResponseValidateXml.response['cadenaOriginalSAT'])
print("\ncadenaOriginalComprobante: ",objResponseValidateXml.response['cadenaOriginalComprobante'])
print("\nuuid: ",objResponseValidateXml.response['uuid'])
print("\nstatusSat: ",objResponseValidateXml.response['statusSat'])
print("\nstatusCodeSat: ",objResponseValidateXml.response['statusCodeSat'])
print("\nstatus: ",objResponseValidateXml.response['status'])
```

**Ejemplo de consumo de la libreria para validación de XML mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Validate.Validate import Validate

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
objValidate = Validate("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseValidateXml = objValidate.ValidateXml(xml)

#Respuesta
print(objResponseValidateXml.get_response())
#Procesamiento de la respuesta

for d in objResponseValidateXml.response["detail"]:
	print("Detail:")
	for detail in d["detail"]:
		print("\tmessage: ", detail["message"])
		print("\tmessageDetail: ", detail["messageDetail"])
		print("\tType: ", str(detail["type"]))
	print("Section: ", d["section"])
print("\ncadenaOriginalSAT: ",objResponseValidateXml.response['cadenaOriginalSAT'])
print("\ncadenaOriginalComprobante: ",objResponseValidateXml.response['cadenaOriginalComprobante'])
print("\nuuid: ",objResponseValidateXml.response['uuid'])
print("\nstatusSat: ",objResponseValidateXml.response['statusSat'])
print("\nstatusCodeSat: ",objResponseValidateXml.response['statusCodeSat'])
print("\nstatus: ",objResponseValidateXml.response['status'])
```

:pushpin: ***NOTA:*** La validación del Xml al no tener "data", ni tampoco "message" obtenemos la response que viene en formato de array asociativo.
</details>

## Consulta Estatus ##

<details>
<summary>
Consulta Estatus SAT
</summary>
Este servicio sirve para consultar el estatus de un CFDI antes y después de enviarlo a cancelar, con él sabremos sí puede ser cancelado de forma directa, o en caso de que se necesite consultar los CFDI relacionados para poder generar la cancelación.

:pushpin: ***NOTA:*** El servicio de consulta es de tipo SOAP y es proporcionado directamente por parte del SAT.

Este metodo recibe los siguientes parametros:
* RFC Emisor
* RFC Receptor
* Total declarado en el comprobante
* UUID del comprobante a consultar
* Url
* Acción

**Ejemplo de consumo de la libreria para la consulta del estatus SAT**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from StatusCfdi.StatusCfdi import StatusCfdi

#Datos
rfc_emisor = "LAN8507268IA" 
rfc_receptor = "LAN7008173R5"
total = "5800.00"
uuid = "eb978000-95c7-4513-8d97-4b59434da45f"
status = StatusCfdi.status(rfc_emisor, rfc_receptor, total, uuid, "https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")

print(status.get_response())
#Datos de respuesta
print(status.get_codigoEstatus())
print(status.get_estado())
print(status.get_esCancelable())
print(status.get_estatusCancelacion())
print(status.get_status_code())
```

</details>

## CFDI Relacionados ##
A través de estos siguientes métodos obtendremos un listado de los UUID que se encuentren relacionados a una factura.

<details>
<summary>
Relacionados por CSD
</summary>

## Relacionados por CSD ##
Este método obtendra un listado de los UUID relacionados mediante CSD

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC del emisor 
* UUID de la factura.
* Certificado en base64
* Llave en base64 
* Contraseña del certificado 


**Ejemplo de consumo de la librería para la consulta de CFDI relacionados por CSD mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Relations.Relations import Relations

relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
response_csd = relations.relations_csd(rfc, uuid, b64_csd, b64_key, password_csd)

if response_csd.get_status() ==  "error":
	print(response_csd.get_message())
	print(response_csd.get_messageDetail())
else:
	print(response_csd.get_data())
```
</details>

<details>
<summary>
Relacionados por PFX
</summary>

## Relacionados por PFX ##
Este método obtendra un listado de los UUID relacionados mediante PFX.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC del emisor
* UUID del comprobante
* Archivo Pfx en Base64
* Contraseña del certificado

**Ejemplo de consumo de la librería para la consulta CFDI relacionados por PFX mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Relations.Relations import Relations

relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
response_pfx = relations.relations_pfx(rfc, uuid, b64_pfx, password_csd)

if response_pfx.get_status() ==  "error":
	print(response_pfx.get_message())
	print(response_pfx.get_messageDetail())
else:
	print(response_pfx.get_data())
```
</details>

<details>
<summary>
Relacionados por UUID
</summary>

## Relacionados por UUID ##
Este método obtendra un listado de los UUID relacionados mediante el UUID de la factura.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC del emisor
* UUID de la factura que ser requiere consultar relacionados

:pushpin: ***NOTA:*** El usuario deberá tener sus certificados en el administrador de timbres para la utilización de este método.

**Ejemplo de consumo de la librería para la consulta CFDI relacionados por UUID mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Relations.Relations import Relations

relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
response_uuid = relations.relations_uuid(rfc, uuid)

if response_uuid.get_status() ==  "error":
	print(response_uuid.get_message())
	print(response_uuid.get_messageDetail())
else:
	print(response_uuid.get_data())
```
</details>


## Consulta solicitudes pendientes Aceptar / Rechazar ##
Este método obtendra una lista de los UUID que tenemos pendientes por aceptar o rechazar.

<details>
  <summary>Ejemplos</summary>

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC Receptor

**Ejemplo de consumo de la librería para la consulta de solicitudes pendientes mediante token**
```py
#importar la clase al inicio de nuestro programa de la siguiente manera:
from Pendings.Pendings import Pendings

pendings = Pendings("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response = pendings.pendings("LAN7008173R5")
print(response.get_status())
```
</details>


## Aceptar / Rechazar ##
Servicio mediante el cual aceptaremos o rechazaremos los UUID.

<details>
<summary>
Aceptar / Rechazar por CSD
</summary>

Método mediante el cual el receptor podrá manifestar la aceptación o rechazo de la solicitud de cancelación mediante CSD.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC del emisor
* Arreglo de objetos donde se especifican los UUID y acción a realizar
* Certificado del receptor en Base64
* Llave(key) del receptor en Base64
* Contraseña del certificado


**Ejemplo de consumo de la librería para la aceptacion/rechazo de la solicitud por CSD mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AcceptReject.AcceptReject import AcceptReject

uuids = [
	{"uuid":"fd74d156-b9b0-44a5-9906-e08182e8363e", "action":"Aceptacion"},			 {"uuid":"26cccb5b-7742-4c54-a031-245a23b8a429", "action":"Rechazo"}
	]
accept_reject = AcceptReject("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response_csd = accept_reject.accept_reject_csd(rfc, uuids, b64_csd, b64_key, password_csd)
print(response_csd.get_status())
```
</details>

<details>
<summary>
Aceptar / Rechazar por PFX
</summary>

Método mediante el cual el receptor podrá manifestar la aceptación o rechazo de la solicitud de cancelación mediante PFX.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC del emisor
* Arreglo de objetos donde se especifican los UUID y acción a realizar
* Archivo Pfx en Base64
* Contraseña del certificado

**Ejemplo de consumo de la librería para la aceptacion/rechazo de la solicitud por PFX mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AcceptReject.AcceptReject import AcceptReject

uuids = [
	{"uuid":"fd74d156-b9b0-44a5-9906-e08182e8363e", "action":"Aceptacion"},			 {"uuid":"26cccb5b-7742-4c54-a031-245a23b8a429", "action":"Rechazo"}
	]
accept_reject = AcceptReject("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response_pfx = accept_reject.accept_reject_pfx(rfc, uuid, b64_pfx, password_csd)
print(response_pfx.get_status())
```
</details>

<details>
<summary>
Aceptar / Rechazar por XML
</summary>

Método mediante el cual el receptor podrá manifestar la aceptación o rechazo de la solicitud de cancelación mediante XML.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* XML con datos requeridos para la aceptacion/rechazo de la cancelación

**Ejemplo de XML**
```xml
<?xml version='1.0' encoding='utf-8'?>
<SolicitudAceptacionRechazo xmlns:xsd='http://www.w3.org/2001/XMLSchema' 
    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' RfcReceptor='LAN7008173R5' RfcPacEnviaSolicitud='DAL050601L35' Fecha='2018-08-22T18:38:05' 
    xmlns='http://cancelacfd.sat.gob.mx'>
    <Folios>
        <UUID>06a46e4b-b154-4c12-bb77-f9a63ed55ff2</UUID>
        <Respuesta>Aceptacion</Respuesta>
    </Folios>
    <Signature xmlns='http://www.w3.org/2000/09/xmldsig#'>
        <SignedInfo>
            <CanonicalizationMethod Algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315' />
            <SignatureMethod Algorithm='http://www.w3.org/2000/09/xmldsig#rsa-sha1' />
            <Reference URI=''>
                <Transforms>
                    <Transform Algorithm='http://www.w3.org/2000/09/xmldsig#enveloped-signature' />
                </Transforms>
                <DigestMethod Algorithm='http://www.w3.org/2000/09/xmldsig#sha1' />
                <DigestValue>AQ36cbqKJKHy5vaS6GhDTWtwKE4=</DigestValue>
            </Reference>
        </SignedInfo>
        <SignatureValue>HVlFUPmRLyxeztem827eaasDObRXi+oqedCNNvDyMsRizqsS99cHt5mJCEE4vWgpDGPGLrph/yd++R4aN+V562DPp9qreFkisFpEvJy5Z8o/KzG7vc5qqaD8z9ohPpRERPHvxFrIm3ryEBqnSV6zqJG02PuxkWvYonVc+B7RdsO5iAiDTMs9guUhOvHBK8BVXQHKCbUAPCp/4YepZ4LUkcdloCAMPsN0x9GaUty2RMtNJuwaRWy+5IIBUCeXXZmQhoQfS0QfPpCByt0ago5v+FocJQiYQrsUV/8mesmNw5JoOCmufQYliQFyZgsstV8+h76dU/rwLr6R8YlFOkTxKg==</SignatureValue>
        <KeyInfo>
            <X509Data>
                <X509IssuerSerial>
                    <X509IssuerName>OID.1.2.840.113549.1.9.2=Responsable: ACDMA, OID.2.5.4.45=SAT970701NN3, L=Coyoacán, S=Distrito Federal, C=MX, PostalCode=06300, STREET='Av. Hidalgo 77, Col. Guerrero', E=asisnet@pruebas.sat.gob.mx, OU=Administración de Seguridad de la Información, O=Servicio de Administración Tributaria, CN=A.C. 2 de pruebas(4096)</X509IssuerName>
                    <X509SerialNumber>3230303031303030303030333030303232383135</X509SerialNumber>
                </X509IssuerSerial>
                <X509Certificate>MIIFxTCCA62gAwIBAgIUMjAwMDEwMDAwMDAzMDAwMjI4MTUwDQYJKoZIhvcNAQELBQAwggFmMSAwHgYDVQQDDBdBLkMuIDIgZGUgcHJ1ZWJhcyg0MDk2KTEvMC0GA1UECgwmU2VydmljaW8gZGUgQWRtaW5pc3RyYWNpw7NuIFRyaWJ1dGFyaWExODA2BgNVBAsML0FkbWluaXN0cmFjacOzbiBkZSBTZWd1cmlkYWQgZGUgbGEgSW5mb3JtYWNpw7NuMSkwJwYJKoZIhvcNAQkBFhphc2lzbmV0QHBydWViYXMuc2F0LmdvYi5teDEmMCQGA1UECQwdQXYuIEhpZGFsZ28gNzcsIENvbC4gR3VlcnJlcm8xDjAMBgNVBBEMBTA2MzAwMQswCQYDVQQGEwJNWDEZMBcGA1UECAwQRGlzdHJpdG8gRmVkZXJhbDESMBAGA1UEBwwJQ295b2Fjw6FuMRUwEwYDVQQtEwxTQVQ5NzA3MDFOTjMxITAfBgkqhkiG9w0BCQIMElJlc3BvbnNhYmxlOiBBQ0RNQTAeFw0xNjEwMjUyMTUyMTFaFw0yMDEwMjUyMTUyMTFaMIGxMRowGAYDVQQDExFDSU5ERU1FWCBTQSBERSBDVjEaMBgGA1UEKRMRQ0lOREVNRVggU0EgREUgQ1YxGjAYBgNVBAoTEUNJTkRFTUVYIFNBIERFIENWMSUwIwYDVQQtExxMQU43MDA4MTczUjUgLyBGVUFCNzcwMTE3QlhBMR4wHAYDVQQFExUgLyBGVUFCNzcwMTE3TURGUk5OMDkxFDASBgNVBAsUC1BydWViYV9DRkRJMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgvvCiCFDFVaYX7xdVRhp/38ULWto/LKDSZy1yrXKpaqFXqERJWF78YHKf3N5GBoXgzwFPuDX+5kvY5wtYNxx/Owu2shNZqFFh6EKsysQMeP5rz6kE1gFYenaPEUP9zj+h0bL3xR5aqoTsqGF24mKBLoiaK44pXBzGzgsxZishVJVM6XbzNJVonEUNbI25DhgWAd86f2aU3BmOH2K1RZx41dtTT56UsszJls4tPFODr/caWuZEuUvLp1M3nj7Dyu88mhD2f+1fA/g7kzcU/1tcpFXF/rIy93APvkU72jwvkrnprzs+SnG81+/F16ahuGsb2EZ88dKHwqxEkwzhMyTbQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAJ/xkL8I+fpilZP+9aO8n93+20XxVomLJjeSL+Ng2ErL2GgatpLuN5JknFBkZAhxVIgMaTS23zzk1RLtRaYvH83lBH5E+M+kEjFGp14Fne1iV2Pm3vL4jeLmzHgY1Kf5HmeVrrp4PU7WQg16VpyHaJ/eonPNiEBUjcyQ1iFfkzJmnSJvDGtfQK2TiEolDJApYv0OWdm4is9Bsfi9j6lI9/T6MNZ+/LM2L/t72Vau4r7m94JDEzaO3A0wHAtQ97fjBfBiO5M8AEISAV7eZidIl3iaJJHkQbBYiiW2gikreUZKPUX0HmlnIqqQcBJhWKRu6Nqk6aZBTETLLpGrvF9OArV1JSsbdw/ZH+P88RAt5em5/gjwwtFlNHyiKG5w+UFpaZOK3gZP0su0sa6dlPeQ9EL4JlFkGqQCgSQ+NOsXqaOavgoP5VLykLwuGnwIUnuhBTVeDbzpgrg9LuF5dYp/zs+Y9ScJqe5VMAagLSYTShNtN8luV7LvxF9pgWwZdcM7lUwqJmUddCiZqdngg3vzTactMToG16gZA4CWnMgbU4E+r541+FNMpgAZNvs2CiW/eApfaaQojsZEAHDsDv4L5n3M1CC7fYjE/d61aSng1LaO6T1mh+dEfPvLzp7zyzz+UgWMhi5Cs4pcXx1eic5r7uxPoBwcCTt3YI1jKVVnV7/w=</X509Certificate>
            </X509Data>
        </KeyInfo>
    </Signature>
</SolicitudAceptacionRechazo>
```

**Ejemplo de consumo de la librería para la aceptacion/rechazo de la solicitud por XML mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AcceptReject.AcceptReject import AcceptReject

#Creamos funcion para abrir nuestro archivo
xml_accept_reject = open_file("file.xml")
accept_reject = AcceptReject("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response_xml = accept_reject.accept_reject_xml(xml_accept_reject)
print(response_xml.get_status())
```
</details>

<details>
<summary>
Aceptar / Rechazar por UUID
</summary>

Método mediante el cual el receptor podrá manifestar la aceptación o rechazo de la solicitud de cancelación mediante UUID.

Este método recibe los siguientes parametros:
* Url Servicios SW
* Usuario y contraseña ò token
* RFC del receptor
* UUID de la factura que se requiere aceptar/rechazar
* Acción que se requiera realizar Aceptacion/Rechazo

:pushpin: ***NOTA:*** El usuario deberá tener sus certificados en el administrador de timbres para la utilización de este método.

**Ejemplo de consumo de la librería para la aceptacion/rechazo de la solicitud por UUID mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from AcceptReject.AcceptReject import AcceptReject

accept_reject = AcceptReject("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
response_uuid = accept_reject.accept_reject_uuid(rfc, uuid, accion)
print(response_uuid.get_status())
```
</details>

## PDF ##

<details>
<summary>
Generar PDF
</summary>

Este método genera y obtiene un pdf en base64 a partir de un documento XML timbrado y una plantilla. Puede ser consumido ingresando tu usuario y contraseña así como tambien ingresando solo el token. Este método recibe los siguientes parámetros:

* Url servicios SW
* Url Api
* Usuario y contraseña o Token
* XML timbrado
* Logo en base 64
* Template id
* Datos extra (opcional)

**Ejemplo de consumo de la libreria para la generación de PDF mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Pdf.Pdf import Pdf
from base64 import b64decode

#Creamos funcion para abrir nuestro archivo
def open_file(pathFile):
    out = open(pathFile,"r", encoding='latin_1', errors='ignore').read()
    return out

#Datos necesarios
xml = open_file("filePdf.xml")
logo = None
extras = None
pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx", "user", "password")
response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
#Obtener respuesta
print("Content B64: ", response.get_content_b64())
print("Content Size Bytes: ", response.get_content_size_bytes())
print("UUID: ", response.get_uuid())
print("Serie: ", response.get_serie())
print("Folio: ", response.get_folio())
print("Stamp Date: ", response.get_stamp_date())
print("Issuer Date: ", response.get_issued_date())
print("RFC Issuer: ", response.get_rfc_issuer())
print("RFC Receptor: ", response.get_rfc_receptor())
print("Total: ", response.get_total())
#Generamos el PDF
bytes = b64decode(response.data["contentB64"], validate=True)
f = open('file.pdf', 'wb')
f.write(bytes)
f.close()
```

**Ejemplo de consumo de la libreria para la generación de PDF mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Pdf.Pdf import Pdf
from base64 import b64decode

#Creamos funcion para abrir nuestro archivo
def open_file(pathFile):
    out = open(pathFile,"r", encoding='latin_1', errors='ignore').read()
    return out

xml = open_file("filePdf.xml")
logo = None
extras = {
        'REFERENCIA': "Referencia de pruebas"
        }
pdf = Pdf("http://services.test.sw.com.mx","https://api.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
response = pdf.generate_pdf(xml,logo,"cfdi40",extras)
#Procesamiento de la respuesta
for Key,Value in response.response["data"].items():
    print (Key,"=",Value)
#Generamos el PDF
bytes = b64decode(response.data["contentB64"], validate=True)
f = open('file.pdf', 'wb')
f.write(bytes)
f.close()
```

:pushpin: ***NOTA:*** Existen varias plantillas de PDF para el CFDI segun el tipo de comprobante, las cuales son las siguientes:

|    Version 4.0     |  Plantilla para el complemento  |   Template Id   |
|--------------------|---------------------------------|-----------------|
| :white_check_mark: | Factura ingreso, egreso         | cfdi40          |
| :white_check_mark: | Nómina                          | payroll40       |
| :white_check_mark: | Pagos                           | payment20       |
| :white_check_mark: | Carta porte                     | billoflading40  |

Para mayor referencia de estas plantillas de PDF, favor de visitar el siguiente [link](https://developers.sw.com.mx/knowledge-base/plantillas-pdf/).
</details>

## Certificados ##
Servicio para gestionar los certificados CSD de tu cuenta.
Para administrar los certificados de manera gráfica, puede hacerlo desde el [Administrador de timbres](https://portal.sw.com.mx/).


<details>
<summary>
Cargar Certificado
</summary>

Método para cargar un certificado en la cuenta.

Este metodo recibe los siguientes parametros:
* Url Servicios SW
* Token
* Tipo de certificado (Default = "stamp") 
* CSD en Base64
* Key en Base64
* Contraseña del certificado

**Ejemplo de consumo de la libreria para la carga de certificado mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Csd.Csd import Csd

csd_obj = Csd("http://services.test.sw.com.mx", None, "user", "password")
response = csd_obj.upload_csd("stamp", b64_csd, b64_key, password_csd)
```
</details>

## TimbradoV4 ##
Servicios de timbrado con servicios adicionales para una mejor experiencia para tu sistema, los headers pueden mezclarse o usarse al mismo tiempo.

### **Email** ###

Este servicio recibe un comprobante CFDI para ser timbrado y recibe un listado de uno o hasta 5 correos electrónicos a los que se requiera enviar el XML timbrado.

Existen varias versiones de respuesta a este método, las cuales puede consultar mas a detalle en el siguiente [link](https://developers.sw.com.mx/knowledge-base/versiones-de-respuesta-timbrado/).

<details>
  <summary>Timbrado XML</summary>

**<br>Ejemplo del consumo de la librería para el servicio StampV4(Email) XML en formato string enviando correos mediante token**
```py
from Stamp.StampV4 import StampV4
from Utils.response_version import ResponseVersion
#Creamos funcion para abrir nuestro archivo
 xml_content = open("prueba.xml", "r", encoding='utf-8').read()
#Creamos instancia y pasamos parametros
 stamp = StampV4("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
 headers = {
                "email": "stamp1@test.com,stamp2@test.com"
           }
response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V2)
print(response.get_data())
print(response.get_status())
```

</details>

<details>
  <summary>Emisión Timbrado XML</summary>

**<br>Ejemplo del consumo de la librería para el servicio Issue V4(Email) XML en formato string enviando correos mediante token**
```py
from Issue.IssueV4 import IssueV4
from Utils.response_version import ResponseVersion
issue = IssueV4("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
             xml_content = open("prueba.xml", "r", encoding='utf-8').read()
            
           headers = {
                "email": "test1@test.com,test2@test.com"
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            print(response.get_data())
            print(response.get_status())
```

</details>

<details>
  <summary>Emisión Timbrado JSON</summary>

  **Ejemplo del consumo de la librería para el servicio IssueV4 (Email) Json en formato string mediante usuario y contraseña.**
```py
from Issue.IssueV4 import IssueV4
from Utils.response_version import ResponseVersion

            issue = IssueV4("http://services.test.sw.com.mx", None, "user", "password")
            json_content =  open_file("cfdi.json")
            
            headers = {
                "email": "test1@test.com,test2@test.com"
            }
            
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)
            print(response.get_data())
            print(response.get_status())
```
</details>

### **CustomId** ###
Este servicio recibe un comprobante CFDI para ser timbrado y que recibe un header conocido como CustomID, el cuál tiene el objetivo de agregar un filtro adicional al timbrado para evitar la duplicidad de timbrado.
El CustomId es un string y el valor es asignado por el usuario, el cual tiene un límite de 100 caracteres.

Existen varias versiones de respuesta a este método, las cuales puede consultar mas a detalle en el siguiente [link](https://developers.sw.com.mx/knowledge-base/versiones-de-respuesta-timbrado/).

<details>
  <summary>Timbrado XML</summary>

**<br>Ejemplo del consumo de la librería para el servicio StampV4(CustomId) XML en formato string mediante usuario y contraseña**
```py
from Stamp.StampV4 import StampV4
from Utils.response_version import ResponseVersion
#Creamos funcion para abrir nuestro archivo
 xml_content = open("prueba.xml", "r", encoding='utf-8').read()
#Creamos instancia y pasamos parametros
 stamp = StampV4("http://services.test.sw.com.mx",None, "user", "password")
 headers = {
                 "customid": "ISS-25-369"
           }
response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V3)
print(response.get_data())
print(response.get_status())
```
</details>

<details>
  <summary>Emisión Timbrado XML</summary>

**<br>Ejemplo del consumo de la librería para el servicio IssueV4 (CustomId)  XML en formato string enviando correos mediante token**
```py
from Issue.IssueV4 import IssueV4
from Utils.response_version import ResponseVersion
issue = IssueV4("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
             xml_content = open("prueba.xml", "r", encoding='utf-8').read()
            
           headers = {
                  "customid": "ISS-25-368"
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            print(response.get_data())
            print(response.get_status())
```

</details>

<details>
 <summary>Emisión Timbrado JSON</summary>

 **Ejemplo del consumo de la librería para el servicio IssueV4 (CustomId) Json en formato string mediante token.**
```py
from Issue.IssueV4 import IssueV4
from Utils.response_version import ResponseVersion

            issue = IssueV4("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
            json_content =  open_file("cfdi.json")
            
            headers = {
                  "customid": "ISS-25-369"
            }
            
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V1)
            print(response.get_data())
            print(response.get_status())
```
</details>

### **PDF** ###
Este servicio recibe un comprobante CFDI para ser timbrado y que recibe un header conocido como extra mediante el cual se confirma la generación de un PDF del CFDI timbrado que será guardado en automático en el ADT.

Existen varias versiones de respuesta a este método, las cuales puede consultar mas a detalle en el siguiente [link](https://developers.sw.com.mx/knowledge-base/versiones-de-respuesta-timbrado/).

***NOTA:*** En caso de que no se cuente con una plantilla PDF customizada los PDF’s serán generados con las plantillas genéricas.

<details>
 <summary>Timbrado XML</summary>

 **Ejemplo del consumo de la librería para el servicio StampV4 (PDF) en formato string mediante usuario y contraseña.** 
```py
from Stamp.StampV4 import StampV4
from Utils.response_version import ResponseVersion
#Creamos funcion para abrir nuestro archivo
 xml_content = open("prueba.xml", "r", encoding='utf-8').read()
#Creamos instancia y pasamos parametros
 stamp = StampV4("http://services.test.sw.com.mx",None, "user", "password")
 headers = {
                 "pdf": "true"
           }
response = stamp.stamp(xml_content, headers=headers, version=ResponseVersion.V2)
print(response.get_data())
print(response.get_status())
```
</details>

<details>
  <summary>Emisión Timbrado XML</summary>

**<br>Ejemplo del consumo de la librería para el servicio IssueV4 (PDF)  XML en formato string enviando correos mediante token**
```py
from Issue.IssueV4 import IssueV4
from Utils.response_version import ResponseVersion
issue = IssueV4("http://services.test.sw.com.mx","T2lYQ0t4L0R....ReplaceForRealToken")
             xml_content = open("prueba.xml", "r", encoding='utf-8').read()
            
           headers = {
                   "pdf": "true"
            }
            
            response = issue.issue_xml(xml_content, headers=headers, version=ResponseVersion.V4)
            print(response.get_data())
            print(response.get_status())
```

</details>


<details>
 <summary>Emisión Timbrado JSON</summary>

 **Ejemplo del consumo de la librería para el servicio IssueV4 (PDF) Json en formato string mediante token**
```py
from Issue.IssueV4 import IssueV4
from Utils.response_version import ResponseVersion

            issue = IssueV4("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
            json_content =  open_file("cfdi.json")
            
            headers = {
                  "pdf": "true"
            }
            
            response = issue.issue_json(json_content, headers=headers, version=ResponseVersion.V4)
            print(response.get_data())
            print(response.get_status())
```
</details>

----------------


Para mayor referencia de un listado completo de los servicios favor de visitar el siguiente [link](http://developers.sw.com.mx/).

Si deseas contribuir a la librería o tienes dudas envianos un correo a **soporte@sw.com.mx**.
