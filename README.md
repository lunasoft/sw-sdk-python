

![Python](https://www.python.org/static/opengraph-icon-200x200.png)
# Requerimientos #

**Python 3** o superior.

[Requests](http://docs.python-requests.org)

**Instalación de librerías requeridas con PIP**

Ejecutar los comandos directamente en la consola tal cual aparecen en la página de la librería requerida, por ejemplo

> pip install requests

# Consumo #

## Authentication ##

Parámetros necesarios: url, user y password.

La clase de authentication, nos sirve para obtener un token de 2 hrs de duración. Podrá ser utilizado en los siguientes servicios para consumo.

**Funciones disponibles**

- Authentication()

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Auth.Auth import Auth
```

Ejemplo de uso

```py
objAuth = Auth("http://services.test.sw.com.mx", None ,"demo","123456789")
objResponseAuth = objAuth.Authentication()
print(objResponseAuth.getToken()+"\nStatus: "+objResponseAuth.getStatus())
```
> Cabe aclarar que Auth recibe un valor "None" en el lugar de donde iría el token para las demás funciones de consumo.

Las funciones utilizables para el objeto obtenido son las siguientes

 > *getTimeExpire()*
 > *getToken()*
 > *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

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
objResponseBal = objBal.AccountBalance()
print(objResponseBal.data)
```

Las funciones utilizables para el objeto obtenido son las siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

## Cancelation ##

Parámetros necesarios: [url, user y password] o [url y token]. Además de los parámetros que nos sean necesarios dependiendo del tipo de cancelación a usar.

La clase de Cancelation nos servirá para cancelar algún comprobante anteriormente ya timbrado, teniendo diversas opciones para poder cancelar dicho documento.

**Funciones disponibles**
 - cancelUuid(rfc, uuid)
 - cancelCsd(rfc, uuid, b64Csd, b64Key, passwordCsd)
 - cancelPfx(rfc, uuid, b64Pfx, passwordCsd)
 - cancelXml(xml)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Cancelation.Cancelation import Cancelation
```

Ejemplo de uso

```py
objCancel = Cancelation("http://services.test.sw.com.mx", token)
objResponseCancelCsd = objCancel.CancelCsd(rfc, uuid, b64Csd, b64Key, passwordCsd)
objResponseCancelUuid = objCancel.CancelUuid(rfc, uuid)
objResponseCancelPfx = objCancel.CancelPfx(rfc, uuid, b64Pfx, passwordCsd)
objResponseCancelXml = objCancel.CancelXml(xmlCancel)
print(objResponseCancelUuid.getStatus())
print(objResponseCancelCsd.getStatus())
print(objResponseCancelPfx.getStatus())
print(objResponseCancelXml.getStatus())
```

Las funciones utilizables para estos objetos de cancelación son los siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

## Issue (Emisión Timbrado) ##

Parámetros necesarios: [user, password y url] o [token y url], así como el XML a timbrar utilizando emisión-timbrado.

La clase Issue nos ayudará a timbrar nuestros documentos XML por medio de emisión-timbrado. A diferencia de la clase Stamp, esta clase además de timbrar el documento le pondrá el sello.

**Funciones disponibles**
- issueV1(xml, b64)
- issueV2(xml, b64)
- issueV3(xml, b64)
- issueV4(xml, b64)
> **b64** es un parámetro opcional y se debe indicar en *true* si el XML va encodeado en base64. De no indicarse, por defecto se tomará el valor de *false*

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Issue.Issue import Issue
```

Ejemplo de uso

```py
objIssue = Issue("http://services.test.sw.com.mx", token)
objResponseIssue = objIssue.IssueV4(xml,True)#XML en Base64
if objResponseIssue.status ==  "error":
	print(objResponseIssue.getMessage())
	print(objResponseIssue.getMessageDetail())
else:
	print(objResponseIssue.getData())
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

## Issue Json (Emisión Timbrado JSON) ##

Parámetros necesarios: [user, password y url] o [token y url], así como el JSON a timbrar utilizando emisión-timbrado.

La clase Issue nos ayudará a timbrar nuestros documentos JSON por medio de emisión-timbrado. A diferencia de la clase Stamp, esta clase además generar el XML y timbrarlo, le pondrá el sello.

**Funciones disponibles**
- IssueJsonV1(json)
- IssueJsonV2(json)
- IssueJsonV3(json)
- IssueJsonV4(json)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Issue.Issue import Issue
```

Ejemplo de uso

```py
objIssue = Issue("http://services.test.sw.com.mx", token)
objResponseIssue = objIssue.IssueJsonV4(open_file("resources\\cfdi.json"))
if objResponseIssue.status ==  "error":
	print(objResponseIssue.getMessage())
	print(objResponseIssue.getMessageDetail())
else:
	print(objResponseIssue.getData())
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

## Stamp ##

Parámetros necesarios: [user, password y url] o [token y url], así como el XML a timbrar.

La clase Stamp se utiliza para el timbrado de documentos XML. El documento deberá venir ya con el sello.

**Funciones disponibles**
- stampV1(xml, b64)
- stampV2(xml, b64)
- stampV3(xml, b64)
- stampV4(xml, b64)

> **b64** es un parámetro opcional y se debe indicar en *true* si el XML va encodeado en base 64. De no indicarse por defecto se tomará el valor de *false*

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Stamp.Stamp import Stamp
```

Ejemplo de uso

```py
objStamp = Stamp("http://services.test.sw.com.mx", token)
objResponseStamp = objStamp.StampV4(open_file("resources\\xml33.xml"))
if objResponseStamp.getStatus() ==  "error":
	print(objResponseStamp.getMessage())
	print(objResponseStamp.getMessageDetail())
else:
	print(objResponseStamp.getData())
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

## Validation ##

Parámetros necesarios: [user, password y url] o [token y url]. Además de parámetros adicionales según sea el caso.

La clase Validation servirá para validar que algunas cosas se encuentren de manera correcta antes de proceder al timbrado del mismo. Por ejemplo, nos pueden ayudar a decir si nuestro XML no tiene algún error, o consultar algún RFC de la lista de contribuyentes obligados.

**Funciones disponibles**
- validateXml(xml)
- validateLrfc(rfc)
- validateLco(noCert)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Validate.Validate import Validate
```

Ejemplo de uso

```py
objValidate = Validate("http://services.test.sw.com.mx", token)
objResponseValidateRFC = objValidate.ValidateLrfc("LAN7008173R5")
print(objResponseValidateRFC.getData())
objResponseValidateNoCert = objValidate.ValidateLco("20001000000300022815")
print(objResponseValidateNoCert.getData())
objResponseValidateXml = objValidate.ValidateXml(open_file("resources\\xml33.xml"))
print(objResponseValidateXml.response)
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

> *getStatus()*
> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

>La validación del Xml al no tener "data", ni tampoco "message" obtenemos la response que viene en formato de array asociativo.

## Estatus CFDI ##

Parámetros necesarios: [rfcEmisor, rfcReceptor, total, uuid, URL del SOAP, Action del SOAP]

La clase Estatus CFDI servirá para verificar el estatus de algún comprobante directamente en el SAT. Este servicio será necesario en el nuevo esquema de cancelación.

**Funciones disponibles**
- status(rfcEmisor, rfcReceptor, total, uuid, URL, Action)


Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from StatusCfdi.StatusCfdi import StatusCfdi
```

Ejemplo de uso

```py
objStatus = StatusCfdi.status("LAN8507268IA", "LAN7008173R5", "5800.00", "6caed040-2f24-4b15-9927-975c2a76fb83", "https://consultaqrfacturaelectronicatest.sw.com.mx/ConsultaCFDIService.svc", "http://tempuri.org/IConsultaCFDIService/Consulta")
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

> *statusCode*
> *response*
> *codigoEstatus*
> *esCancelable*
> *estado*
> *estatusCancelacion*

## Consulta Documentos Relacionados ##
Parámetros necesarios: [url, user y password] o [url y token]. Además de los parámetros que nos sean necesarios dependiendo del tipo de método a usar.

La clase de Relations nos servirá para consultar los documentos que existen haciendo relación al documento consultado.

**Funciones disponibles**
 - RelationsUuid(rfc, uuid)
 - RelationsCsd(rfc, uuid, b64Csd, b64Key, passwordCsd)
 - RelationsPfx(rfc, uuid, b64Pfx, passwordCsd)
 - RelationsXml(xml)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Relations.Relations import Relations
```

Ejemplo de uso

```py
objrelations = Relations("http://services.test.sw.com.mx", token)
objResponseRelationsCSD = objrelations.RelationsCsd(rfc, uuid, b64Csd, b64Key, passwordCsd)
objResponseRelationsUuid = objrelations.RelationsUuid(rfc, uuid)
objResponseRelationsPfx = objrelations.RelationsPfx(rfc, uuid, b64Pfx, passwordCsd)
objResponseRelationsXml = objrelations.RelationsXml(xmlRelations)
print(objResponseRelationsUuid.getStatus())
print(objResponseCancelCSD.getStatus())
print(objResponseRelationsPfx.getStatus())
print(objResponseRelationsXml.getStatus())
```

Las funciones utilizables para estos objetos de relacionados son los siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*

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
objPendings = Pendings("http://services.test.sw.com.mx", token)
objResponse = objPendings.pendings("LAN7008173R5")
print(objResponse.getStatus())
```

##  Aceptar/Rechazar Cancelación ##
Parámetros necesarios: [url, user y password] o [url y token]. Además de los parámetros que nos sean necesarios dependiendo del tipo de cancelación a usar.

La clase de AcceptReject nos servirá para cancelar algún comprobante pendiente, teniendo diversas opciones para poder cancelar dicho documento.

**Funciones disponibles**
 - AcceptRejectUuid(rfc, uuid)
 - AcceptRejectCsd(rfc, uuids, b64Csd, b64Key, passwordCsd)
 - AcceptRejectPfx(rfc, uuids, b64Pfx, passwordCsd)
 - AcceptRejectXml(xml)
> Tener en cuenta que los métodos que se consumen por CSD o PFX se envía un JSON Array como el siguiente:
>  - uuids = [{"uuid":"fd74d156-b9b0-44a5-9906-e08182e8363e", "action":"Aceptacion"},{"uuid":"26cccb5b-7742-4c54-a031-245a23b8a429", "action":"Rechazo"}]

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from AcceptReject.AcceptReject import AcceptReject
```

Ejemplo de uso

```py
objAcceptReject = AcceptReject("http://services.test.sw.com.mx", token)
uuids = [{"uuid":"fd74d156-b9b0-44a5-9906-e08182e8363e", "action":"Aceptacion"}]
objResponseCsd = objAcceptReject.AcceptRejectCsd(rfc,uuids,b64CSD), b64Key,"12345678a")
objResponseUuid = objAcceptReject.AcceptRejectUuid(rfc, uuid)
objResponsePfx = objAcceptReject.AcceptRejectPfx(rfc, uuid, b64Pfx, passwordCsd)
objResponseXml = objAcceptReject.AcceptRejectXml(xmlAcceptReject)
print(objResponseUuid.getStatus())
print(objResponseCsd.getStatus())
print(objResponsePfx.getStatus())
print(objResponseXml.getStatus())
```

Las funciones utilizables para estos objetos de accept/reject son los siguientes

> *getMessage()*
> *getMessageDetail()*
> *getData()*
> *getResponse()*
> *getStatus()*


## Procesamiento de las respuestas ##
Cuando obtenemos un "data", éste viene en formato array asociativo. A continuación expondré ejemplos de uso.

**Ejemplo 1:**

Tratamiento de los datos de la validación de Xml aquí un ejemplo.
```py
objValidate = Validate("http://services.test.sw.com.mx", token)
objResponseValidateXml = objValidate.ValidateXml(open_file("resources\\xml33.xml"))
for d in objResponseValidateXml.response["detail"]:
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


**Ejemplo 2:**

Tratamiento de los datos de la validación de Lco

```py
objValidate = Validate("http://services.test.sw.com.mx", token)
objResponseValidateNoCert = objValidate.ValidateLco("20001000000300022815")
respuesta = objResponseValidateNoCert.getData()
numeroCertificado = respuesta["noCertificado"] #contiene 20001000000300022815
rfc = respuesta["rfc"] #contiene LAN7008173R5
#fechas de validez del certificado
fechaInicio = respuesta["fechaInicio"]#contiene '2016-10-25T04:52:11'
fechaFin = respuesta["fechaFinal"]#contiene '2020-10-25T03:52:11'
```

Con esto podemos tratar los datos de manera interna a nuestra conveniencia.