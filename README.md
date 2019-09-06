



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

- authentication()

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Auth.auth import Auth
```

Ejemplo de uso

```py
objAuth = Auth("http://services.test.sw.com.mx", None ,"demo","123456789")
objResponseAuth = objAuth.authentication()
print(objResponseAuth.get_token()+"\nStatus: "+objResponseAuth.get_status())
```
> Cabe aclarar que Auth recibe un valor "None" en el lugar de donde iría el token para las demás funciones de consumo.

Las funciones utilizables para el objeto obtenido son las siguientes

>- *get_time_expire()*
>- *get_token()*
>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Balance ##

Parámetros necesarios: [url, user y password] o [url y token].

La clase de Balance nos ayuda a obtener información referente a nuestra cuenta. Así sabremos cuando nos quedan pocos timbres o cuantos tenemos asignados, etc. 

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Balance.balance import Balance
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

**Funciones disponibles**
 - cancel_uuid(rfc, uuid)
 - cancel_csd(rfc, uuid, b64_cert, b64_key, password)
 - cancel_pfx(rfc, uuid, b64_pfx, password)
 - cancel_xml(xml)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Cancelation.cancelation import Cancelation
```

Ejemplo de uso

```py
cancel = Cancelation("http://services.test.sw.com.mx", token)
response_csd = cancel.cancel_csd(rfc, uuid, b64_csd, b64_key, password_csd)
response_uuid = cancel.cancel_uuid(rfc, uuid)
response_pfx = cancel.cancel_pfx(rfc, uuid, b64_pfx, password_csd)
response_xml = cancel.cancel_xml(xml_cancel)
print(response_csd.get_status())
print(response_uuid.get_status())
print(response_pfx.get_status())
print(response_xml.get_status())
```

Las funciones utilizables para estos objetos de cancelación son los siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Issue (Emisión Timbrado) ##

Parámetros necesarios: [user, password y url] o [token y url], así como el XML a timbrar utilizando emisión-timbrado.

La clase Issue nos ayudará a timbrar nuestros documentos XML por medio de emisión-timbrado. A diferencia de la clase Stamp, esta clase además de timbrar el documento le pondrá el sello.

**Funciones disponibles**
- issue_v1(xml, b64)
- issue_v2(xml, b64)
- issue_v3(xml, b64)
- issue_v4(xml, b64)
> **b64** es un parámetro opcional y se debe indicar en *true* si el XML va encodeado en base64. De no indicarse, por defecto se tomará el valor de *false*

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Issue.issue import Issue
```

Ejemplo de uso

```py
issue = Issue("http://services.test.sw.com.mx", token)
response = issue.issue_v4(xml, True)#XML en Base64
if response.status ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Issue Json (Emisión Timbrado JSON) ##

Parámetros necesarios: [user, password y url] o [token y url], así como el JSON a timbrar utilizando emisión-timbrado.

La clase Issue nos ayudará a timbrar nuestros documentos JSON por medio de emisión-timbrado. A diferencia de la clase Stamp, esta clase además generar el XML y timbrarlo, le pondrá el sello.

**Funciones disponibles**
- issue_json_v1(json)
- issue_json_v2(json)
- issue_json_v3(json)
- issue_json_v4(json)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Issue.issue import Issue
```

Ejemplo de uso

```py
issue = Issue("http://services.test.sw.com.mx", token)
response = issue.issue_json_v4(open_file("resources\\cfdi.json"))
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Stamp ##

Parámetros necesarios: [user, password y url] o [token y url], así como el XML a timbrar.

La clase Stamp se utiliza para el timbrado de documentos XML. El documento deberá venir ya con el sello.

**Funciones disponibles**
- stamp_v1(xml, b64)
- stamp_v2(xml, b64)
- stamp_v3(xml, b64)
- stamp_v4(xml, b64)

> **b64** es un parámetro opcional y se debe indicar en *true* si el XML va encodeado en base 64. De no indicarse por defecto se tomará el valor de *false*

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Stamp.stamp import Stamp
```

Ejemplo de uso

```py
stamp = Stamp("http://services.test.sw.com.mx", token)
response = stamp.StampV4(open_file("resources\\xml33.xml"))
if response.get_status() ==  "error":
	print(response.get_message())
	print(response.get_messageDetail())
else:
	print(response.get_data())
```

Las funciones correspondientes al objeto que regresan estas funciones son las siguientes

>- *get_message()*
>- *get_messageDetail()*
>- *get_data()*
>- *get_response()*
>- *get_status()*
>- *get_status_code()*

## Validation ##

Parámetros necesarios: [user, password y url] o [token y url]. Además de parámetros adicionales según sea el caso.

La clase Validation servirá para validar que algunas cosas se encuentren de manera correcta antes de proceder al timbrado del mismo. Por ejemplo, nos pueden ayudar a decir si nuestro XML no tiene algún error, o consultar algún RFC de la lista de contribuyentes obligados.

**Funciones disponibles**
- validate_xml(xml)
- validate_lrfc(rfc)
- validate_lco(noCert)

Importar la clase al comienzo de nuestro programa de la siguiente manera

```py
from Validate.validate import Validate
```

Ejemplo de uso

```py
validate = Validate("http://services.test.sw.com.mx", token)
response_rfc = validate.Validate_lrfc("LAN7008173R5")
print(response_rfc.get_data())
response_lco = validate.Validate_lco("20001000000300022815")
print(response_lco.get_data())
response_xml = validate.Validate_xml(open_file("resources\\xml33.xml"))
print(response_xml.get_response())
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
from StatusCfdi.status_cfdi import StatusCfdi
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
from Relations.relations import Relations
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
from Pendings.pendings import Pendings
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
from AcceptReject.accept_reject import AcceptReject
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


**Ejemplo 2:**

Tratamiento de los datos de la validación de lco

```py
validate = Validate("http://services.test.sw.com.mx", token)
response_lco = validate.validate_lco("20001000000300022815")
respuesta = response_lco.get_data()
numeroCertificado = respuesta["noCertificado"] #contiene 20001000000300022815
rfc = respuesta["rfc"] #contiene LAN7008173R5
#fechas de validez del certificado
fechaInicio = respuesta["fechaInicio"]#contiene '2016-10-25T04:52:11'
fechaFin = respuesta["fechaFinal"]#contiene '2020-10-25T03:52:11'
```

Con esto podemos tratar los datos de manera interna a nuestra conveniencia.