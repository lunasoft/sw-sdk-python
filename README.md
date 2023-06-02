# SDK python

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
---

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

:pushpin: ***NOTA:***  Cabe aclarar que Auth recibe un valor "None" en el lugar de donde iría el token para las demás funciones de consumo.


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
response = stamp.StampV4(open_file(xml))
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
response = stamp.StampV4(xml)
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
response = stamp.StampV4(encoded.decode(),True)
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
response = issue.issue_v4(xml)
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
response = issue.issue_v4(xml)
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
response = issue.issue_v4(encoded.decode(), True)
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
response = issue.issue_json_v4(json)
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
response = issue.issue_json_v4(json)
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

## Balance ##

Parámetros necesarios: [url, user y password] o [url y token].

La clase de Balance nos ayuda a obtener información referente a nuestra cuenta. Así sabremos cuando nos quedan pocos timbres o cuantos tenemos asignados, etc. 

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Balance.Balance import Balance
```

Ejemplo de uso

```py
objBal = Balance("http://services.test.sw.com.mx", token)
objResponseBal = objBal.account_balance()
print(objResponseBal.data)
```

Las funciones utilizables para el objeto obtenido son las siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Cancelation ##

Parámetros necesarios: [url, user y password] o [url y token]. Además de los parámetros que nos sean necesarios dependiendo del tipo de cancelación a usar.

La clase de Cancelation nos servirá para cancelar algún comprobante anteriormente ya timbrado, teniendo diversas opciones para poder cancelar dicho documento.

Funciones disponibles

 - cancelUuid(rfc, uuid, motivo, foliosustitucion)
 - cancelCsd(uuid, passwordCsd, rfc, motivo, foliosustitucion, b64Csd, b64Key)
 - cancelPfx(uuid, passwordCsd, rfc, motivo, foliosustitucion, b64Pfx)
 - cancelXml(xml)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Cancelation.Cancelation import Cancelation
```

Ejemplo de uso

```py
objCancel = Cancelation("http://services.test.sw.com.mx", token)
objResponseCancelCSD = objCancel.CancelCsd(uuid, passwordCsd, rfc, motivo, foliosust, b64Csd, b64Key)
objResponseCancelUuid  = objCancel.CancelUuid(rfc, uuid, motivo, foliosust)
objResponseCancelPfx  = objCancel.CancelPfx(uuid, passwordCsd, rfc, motivo, foliosust, b64Pfx)
objResponseCancelXml  = objCancel.CancelCsd(xmlCancel)
print(objResponseCancelUUID.getStatus())
print(objResponseCancelCSD.getStatus())
print(objResponseCancelPFX.getStatus())
print(objResponseCancelXML.getStatus())
```

Las funciones utilizables para estos objetos de cancelación son los siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Validation ##

Parámetros necesarios: [user, password y url] o [token y url]. Además de parámetros adicionales según sea el caso.

La clase Validation servirá para validar que algunas cosas se encuentren de manera correcta antes de proceder al timbrado del mismo. Por ejemplo, nos pueden ayudar a decir si nuestro XML no tiene algún error.

Funciones disponibles

- validateXml(xml)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Validate.Validate import Validate
```

Ejemplo de uso

```py
objValidate = Validate("http://services.test.sw.com.mx", token)
objResponseValidateXml = objValidate.ValidateXml(open_file("resources\\xml33.xml"))
print(objResponseValidateXml.response)
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

>La validación del Xml al no tener "data", ni tampoco "message" obtenemos la response que viene en formato de array asociativo.

## Estatus CFDI ##

Parámetros necesarios: [rfcEmisor, rfcReceptor, total, uuid, URL del SOAP, Action del SOAP]

La clase Estatus CFDI servirá para verificar el estatus de algún comprobante directamente en el SAT. Este servicio será necesario en el nuevo esquema de cancelación.

**Funciones disponibles**
- status(rfc_emisor, rfc_receptor, total, uuid, url, soap_action)


Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from StatusCfdi.StatusCfdi import StatusCfdi
```

Ejemplo de uso

```py
status = StatusCfdi.status("LAN8507268IA", "LAN7008173R5", "5800.00", "eb978000-95c7-4513-8d97-4b59434da45f", "https://pruebacfdiconsultaqr.cloudapp.net/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

>- *get_status_code()*
>- *get_response()*
>- *get_codigoEstatus()*
>- *get_esCancelable()*
>- *get_estado()*
>- *get_estatusCancelacion()*

## Consulta Documentos Relacionados ##
Parámetros necesarios: [url, user y password] o [url y token]. Además de los parámetros que nos sean necesarios dependiendo del tipo de método a usar.

La clase de Relations nos servirá para consultar los documentos que existen haciendo relación al documento consultado.

**Funciones disponibles**
 - relations_uuid(rfc, uuid)
 - relations_csd(rfc, uuid, b64_csd, b64_key, password_csd)
 - relations_pfx(rfc, uuid, b64_pfx, password_csd)
 - relations_xml(xml)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Relations.Relations import Relations
```

Ejemplo de uso

```py
relations = Relations("http://services.test.sw.com.mx", None, "demo", "123456789")
response_csd = relations.relations_csd(rfc, uuid, b64_csd, b64_key, password_csd)
response_uuid = relations.relations_uuid(rfc, uuid)
response_pfx = relations.relations_pfx(rfc, uuid, b64_pfx, password_csd)
response_xml = relations.relations_xml(xml_relations)
print(response_csd.get_status())
print(response_uuid.get_status())
print(response_pfx.get_status())
print(response_xml.get_status())
```

Las funciones utilizables para estos objetos de relacionados son los siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

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
