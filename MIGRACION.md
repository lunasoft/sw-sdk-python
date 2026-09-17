# Migración a la 1.0

La 1.0 deja la API pública con una sola convención: `snake_case`, en inglés, sin typos.
**No se conservaron alias con los nombres anteriores**, de modo que el código que hoy
consume la librería necesita actualizarse. Este documento lista cada cambio.

Lo que **no** cambió: las llaves del JSON que devuelve el servicio. `messageDetail`,
`codStatus`, `contentB64`, `resultado` y demás siguen llegando con ese nombre, así que
leer la respuesta cruda con `response.get_response()` o `response.data["contentB64"]`
funciona igual que antes. Lo que se renombró son los atributos y métodos de la librería.

---

## Rutas de importación

| Antes | Ahora |
|---|---|
| `from Stamp_Retentions.Stamp_Retentions import Stamp_Retentions` | `from StampRetentions.StampRetentions import StampRetentions` |
| `from Cancelation_Retentions.CancelationRetentions import CancelationRetentions` | `from CancelationRetentions.CancelationRetentions import CancelationRetentions` |

Los directorios `Stamp_Retentions/` y `Cancelation_Retentions/` pasaron a
`StampRetentions/` y `CancelationRetentions/`. Eran los dos únicos paquetes con guion
bajo de los diecisiete del proyecto.

## Clases

| Antes | Ahora |
|---|---|
| `Stamp_Retentions` | `StampRetentions` |
| `Stamp_RetentionsRequest` | `StampRetentionsRequest` |
| `Stamp_RetentionsResponse` | `StampRetentionsResponse` |

## Métodos de servicio

### `Cancelation`

| Antes | Ahora |
|---|---|
| `CancelXml(xmlCancel)` | `cancel_xml(xmlCancel)` |
| `CancelCsd(...)` | `cancel_csd(...)` |
| `CancelPfx(...)` | `cancel_pfx(...)` |
| `CancelUuid(...)` | `cancel_uuid(...)` |

### `CancelationRetentions`

Quedan con el mismo nombre que sus equivalentes de `Cancelation`.

| Antes | Ahora |
|---|---|
| `CancelaUno(xmlCancel)` | `cancel_xml(xmlCancel)` |
| `CancelaUnoCSD(...)` | `cancel_csd(...)` |
| `CancelaUnoPFX(...)` | `cancel_pfx(...)` |

### `Validate`

| Antes | Ahora |
|---|---|
| `ValidateXml(xml, status=None)` | `validate_xml(xml, status=None)` |

### `AccountUser`

Las consultas que devuelven varias cuentas quedan en plural y las que devuelven una en
singular, igual que el servicio.

| Antes | Ahora |
|---|---|
| `getUser_all(...)` | `get_users(...)` |
| `getUser_by_idUser(idUser, ...)` | `get_user_by_id(idUser, ...)` |
| `getUser_by_email(email, ...)` | `get_user_by_email(email, ...)` |
| `getUser_by_taxId(taxId, ...)` | `get_user_by_tax_id(taxId, ...)` |
| `getUser_by_isActive(isActive, ...)` | `get_users_by_is_active(isActive, ...)` |
| `getUser_by_name(name, ...)` | `get_user_by_name(name, ...)` |

### `StampRetentions`

| Antes | Ahora |
|---|---|
| `stamp_retetions_v3(xml)` | `stamp_retentions_v3(xml)` |

Además, `token` dejó de ser posicional obligatorio y ahora es `token=None`, como en los
otros quince servicios. Construirlo con usuario y contraseña ya no obliga a pasar `None`
de relleno:

```py
#Antes
stamp = StampRetentions(url, None, "user", "password")
#Ahora también vale
stamp = StampRetentions(url, user="user", password="password")
```

Las llamadas que ya pasaban token siguen funcionando igual.

### `RequestHelper`

| Antes | Ahora |
|---|---|
| `post_json_request_Without_Headers(...)` | `post_json_request_without_headers(...)` |

## Parámetro `urlApi`

Los cuatro servicios que reciben dos URL (`AccountUser`, `Balance`, `Pdf`, `Storage`)
renombraron el parámetro `urlApi` a `url_api`. **Rompe sólo a quien lo pase por nombre**,
no por posición:

```py
#Antes
pdf = Pdf(url, urlApi="https://api.test.sw.com.mx", token=token)
#Ahora
pdf = Pdf(url, url_api="https://api.test.sw.com.mx", token=token)

#Por posición no cambia nada
pdf = Pdf(url, "https://api.test.sw.com.mx", token)
```

## Respuestas

### `Response` (clase base: alcanza a todas las respuestas)

| Antes | Ahora |
|---|---|
| `messageDetail` | `message_detail` |
| `get_messageDetail()` | `get_message_detail()` |

### `AcceptRejectResponse` y `RelationsResponse`

| Antes | Ahora |
|---|---|
| `codStatus` | `cod_status` |
| `get_codStatus()` | `get_cod_status()` |

### `RelationsResponse`

| Antes | Ahora |
|---|---|
| `uuid_consultado` / `get_uuid_consultado()` | `queried_uuid` / `get_queried_uuid()` |
| `resultado` / `get_resultado()` | `result` / `get_result()` |
| `uuids_relacionados_padres` / `get_uuids_relacionados_padres()` | `parent_related_uuids` / `get_parent_related_uuids()` |
| `uuids_relacionados_hijos` / `get_uuids_relacionados_hijos()` | `child_related_uuids` / `get_child_related_uuids()` |

### `StatusCfdiResponse`

| Antes | Ahora |
|---|---|
| `codigoEstatus` / `get_codigoEstatus()` / `search_codigoEstatus()` | `status_code_sat` / `get_status_code_sat()` / `search_status_code_sat()` |
| `esCancelable` / `get_esCancelable()` / `search_esCancelable()` | `is_cancelable` / `get_is_cancelable()` / `search_is_cancelable()` |
| `estado` / `get_estado()` / `search_estado()` | `state` / `get_state()` / `search_state()` |
| `estatusCancelacion` / `get_estatusCancelacion()` / `search_estatusCancelacion()` | `cancelation_status` / `get_cancelation_status()` / `search_cancelation_status()` |

### `PdfResponse`

Los getters (`get_content_b64()`, `get_stamp_date()`, …) **ya estaban** en `snake_case` y
no cambiaron. Lo que cambió son los atributos, para quien los leía directo.

| Antes | Ahora |
|---|---|
| `contentB64` | `content_b64` |
| `contentSizeBytes` | `content_size_bytes` |
| `stampDate` | `stamp_date` |
| `issuedDate` | `issued_date` |
| `rfcIssuer` | `rfc_issuer` |
| `rfcReceptor` | `rfc_receptor` |

### `BalanceResponse`

| Antes | Ahora |
|---|---|
| `LastTransaction.idUSer` | `LastTransaction.idUser` |

Era un typo. Se corrige a `idUser`, que es como lo manda el servicio.

---

## Corrección de comportamiento incluida en estos renombres

`PdfResponse` y `ValidateResponse` asignaban `self.statusCode` mientras heredaban
`get_status_code()`, que lee `self.status_code`. **El getter devolvía `None` siempre** y
el código HTTP no había forma de leerlo por la API:

```py
#Antes
response.get_status_code()   # None
#Ahora
response.get_status_code()   # 200
```

`StatusCfdiResponse` tenía el mismo atributo mal escrito en su rama `except`, y también
quedó corregido.

Si tu código sorteaba el problema leyendo `response.statusCode` directo, ahora tiene que
leer `response.get_status_code()` o `response.status_code`.
