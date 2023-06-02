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

### Compatibilidad
- CFDI 3.3 (Complemento de nóminas)
- CFDI 4.0
- Python 3 o superior

### Dependencias
- **Python 3** o superior.
- [Requests](http://docs.python-requests.org)

### Documentación
* [Inicio Rápido](https://developers.sw.com.mx/knowledge-base/conoce-el-proceso-de-integracion-en-solo-7-pasos/)
* [Documentacion Oficial Servicios](http://developers.sw.com.mx)


### Instalación

Ejecutar los comandos directamente en la consola tal cual aparecen en la página de la librería requerida, por ejemplo

 ```py
pip install requests
```

### Implementación

La librería contara con los servicios principales como lo son Timbrado de CFDI, Cancelación, Consulta estatus CFDI, etc.


## Autenticaci&oacute;n ##
El servicio de Autenticación es utilizado principalmente para obtener el **token** el cual sera utilizado para poder timbrar nuestro CFDI (xml) ya emitido (sellado), para poder utilizar este servicio es necesario que cuente con un **usuario** y **contraseña** para posteriormente obtenga el token, usted puede utilizar los que estan en este ejemplo para el ambiente de **Pruebas**.

:pushpin: ***NOTA:*** La clase de authentication, nos sirve para obtener un token de 2 hrs de duración.

Parámetros necesarios: 
- Url Servicios SW
- Usuario y contraseña

**Ejemplo de consumo de la librería para obtener token**
 ```py
 #Importar la clase al comienzo de nuestro programa de la siguiente manera
 from Auth.Auth import Auth

 objAuth = Auth("http://services.test.sw.com.mx", None ,"user","password")
 objResponseAuth = objAuth.Authentication()
 
 if objResponseAuth.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(objResponseAuth.get_token())

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
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Stamp.Stamp import Stamp

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
#Creamos instancia y pasamos parametros
stamp = Stamp("http://services.test.sw.com.mx", None, "user", "password")
response = stamp.stamp_v1(open_file(xml))
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

**Ejemplo de consumo de la libreria para timbrar XML en formato string utilizando token** [¿Como obtener token?](http://developers.sw.com.mx/knowledge-base/generar-un-token-infinito/)
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Stamp.Stamp import Stamp

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
#Creamos instancia y pasamos parametros
stamp = Stamp("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
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
xml = open_file("file.xml")
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
* Usuario y contraseña
* Url Servicios SW
* Certificado (.cer)
* Key (.key)
* RFC emisor
* Password del archivo key
* UUID
* Motivo
* Folio Sustitución (Si el motivo es 01)

**Ejemplo de consumo de la libreria para cancelar con CSD con motivo de cancelación 02 sin relación a documento mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

#Datos
uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "02"
foliosustitucion = "01724196-ac5a-4735-b621-e3b42bcbb459"
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
foliosustitucion = None
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelCSD = objCancel.CancelCsd(uuid, passwordCsd, rfc, motivo, foliosust, b64Csd, b64Key)

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
* Usuario y contraseña
* Url Servicios SW
* Archivo PFX 
* RFC emisor
* Password (CSD)
* UUID
* Motivo
* Folio Sustitución

**Ejemplo de consumo de la libreria para cancelar con PFX con motivo de cancelación 02 sin relación a documento mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Cancelation.Cancelation import Cancelation

uuid = "8D93A20F-E9EF-42CA-A2B9-2986A352DCEC"
motivo = "02"
foliosustitucion = "01724196-ac5a-4735-b621-e3b42bcbb459"
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelPfx = objCancel.CancelPfx(rfc, b64Pfx, cPassword, motivo, foliosustitucion)

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
foliosustitucion = None
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelPfx = objCancel.CancelPfx(rfc, b64Pfx, cPassword, motivo, foliosustitucion)

if objResponseCancelPfx .get_status() ==  "error":
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
* Usuario y contraseña
* Url Servicios SW
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

if objResponseCancelPfx .get_status() ==  "error":
	print(objResponseCancelPfx.get_message())
	print(objResponseCancelPfx.get_messageDetail())
else:
	print(objResponseCancelPfx.get_data())
```
</details>

<details>
<summary>
Cancelacion por UUID
</summary>

Como su nombre lo indica, este método realiza la cancelacion mediante el UUID a cancelar.

Este método recibe los siguientes parametros:
* Usuario y contraseña
* Url Servicios SW
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
foliosustitucion = "01724196-ac5a-4735-b621-e3b42bcbb459"
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
foliosustitucion = None
objCancel = Cancelation("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseCancelUuid = objCancel.CancelUuid(uuid, rfc, motivo, foliosustitucion)

if objResponseCancelUuid.get_status() ==  "error":
	print(objResponseCancelUuid.get_message())
	print(objResponseCancelUuid.get_messageDetail())
else:
	print(objResponseCancelUuid.get_data())
```
</details>

## Balance ##

<details>
<summary>
Consultar saldo
</summary>

Servicio mediante el cual puedes realizar la consulta de tu saldo para consumir los servicios de SW.


Este método recibe los siguientes parametros:
* Usuario y contraseña ó token
* Url Servicios SW

**Ejemplo de consumo de la libreria para consultar saldo mediante usuario y contraseña**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBal = Balance("http://services.test.sw.com.mx", None ,"user","password")
objResponseBal = objBal.account_balance()
if objResponseBal.get_status() ==  "error":
	print(objResponseBal.get_message())
	print(objResponseBal.get_messageDetail())
else:
	print(objResponseBal.get_data())
```

**Ejemplo de consumo de la libreria para consultar saldo mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Balance.Balance import Balance

objBal = Balance("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseBal = objBal.account_balance()
if objResponseBal.get_status() ==  "error":
	print(objResponseBal.get_message())
	print(objResponseBal.get_messageDetail())
else:
	print(objResponseBal.get_data())
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

print(objResponseValidateXml.get_response())
```

**Ejemplo de consumo de la libreria para validación de XML mediante token**
```py
#Importar la clase al comienzo de nuestro programa de la siguiente manera
from Validate.Validate import Validate

#Creamos funcion para abrir nuestro archivo
xml = open_file("file.xml")
objValidate = Validate("http://services.test.sw.com.mx", "T2lYQ0t4L0R....ReplaceForRealToken")
objResponseValidateXml = objValidate.ValidateXml(xml)

print(objResponseValidateXml.get_response())
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
```
Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

>- *get_status_code()*
>- *get_response()*
>- *get_codigoEstatus()*
>- *get_esCancelable()*
>- *get_estado()*
>- *get_estatusCancelacion()*

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
* UUID del comprobante
* RFC del emisor
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


## Consulta Solicitudes Pendientes ##
Parámetros necesarios: [url, user y password] o [url y token]. Además del RFC del cual obtendremos la lista de uuid que tiene pendiente por Aceptar o Rechazar.

La clase de Pendings nos servirá para conocer la lista de uuids que un RFC como cliente tiene pendientes de aceptar o rechazar en el nuevo esquema de cancelaciones.

**Funciones disponibles**
- pendings(rfc)

importar la clase al inicio de nuestro programa de la siguiente manera:

```py
from Pendings.Pendings import Pendings
```

Ejemplo de uso

```py
pendings = Pendings("http://services.test.sw.com.mx", token)
response = pendings.pendings("LAN7008173R5")
print(response.get_status())
```

##  Aceptar/Rechazar Cancelación ##
Parámetros necesarios: [url, user y password] o [url y token]. Además de los parámetros que nos sean necesarios dependiendo del tipo de cancelación a usar.

La clase de AcceptReject nos servirá para cancelar algún comprobante pendiente, teniendo diversas opciones para poder cancelar dicho documento.

**Funciones disponibles**
 - accept_reject_uuid(rfc, uuid)
 - accept_reject_csd(rfc, uuids, b64_csd, b64_key, password_csd)
 - accept_reject_pfx(rfc, uuids, b64_pfx, password_csd)
 - accept_reject_xml(xml)
> Tener en cuenta que los métodos que se consumen por CSD o PFX se envía un JSON Array como el siguiente:
>  - uuids = [{"uuid":"fd74d156-b9b0-44a5-9906-e08182e8363e", "action":"Aceptacion"},{"uuid":"26cccb5b-7742-4c54-a031-245a23b8a429", "action":"Rechazo"}]

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from AcceptReject.AcceptReject import AcceptReject
```

Ejemplo de uso

```py
accept_reject = AcceptReject("http://services.test.sw.com.mx", token)
uuids = [{"uuid":"fd74d156-b9b0-44a5-9906-e08182e8363e", "action":"Aceptacion"}]
response_csd = accept_reject.accept_reject_csd(rfc, uuids, b64_csd, b64_key, password_csd)
response_uuid = accept_reject.accept_reject_uuid(rfc, uuid)
response_pfx = accept_reject.accept_reject_pfx(rfc, uuid, b64_pfx, password_csd)
response_xml = accept_reject.accept_reject_xml(xml_accept_reject)
print(response_uuid.get_status())
print(response_csd.get_status())
print(response_pfx.get_status())
print(response_xml.get_status())
```

Las funciones utilizables para estos objetos de accept/reject son los siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*


## Procesamiento de las respuestas ##
Cuando obtenemos un "data", éste viene en formato array asociativo. A continuación expondré ejemplos de uso.

**Ejemplo 1:**

Tratamiento de los datos de la validación de xml aquí un ejemplo.
```py
validate = Validate("http://services.test.sw.com.mx", token)
response_xml = validate.validate_xml(open_file("resources\\xml33.xml"))
for d in response_xml.response["detail"]:
	print("Detail:")
	for detail in d["detail"]:
		print("\tmessage: "+detail["message"])
		print("\tmessageDetail: "+detail["messageDetail"])
		print("\tType: "+str(detail["type"]))
	print("Section: "+d["section"])
```

**Output**

> Detail:
>         message: OK
>         messageDetail: Validacion de Estructura Correcta
>         Type: 1 Section: CFDI33 - Validacion de Estructura Detail:
>         message: OK
>         messageDetail: Validaciones Proveedor Comprobante ( CFDI33 ) Correcta
>         Type: 1 Section: CFDI33 - Validaciones Proveedor Comprobante  ( CFDI33 )
