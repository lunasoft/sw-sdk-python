import requests
from xml.sax.saxutils import escape
from StatusCfdi.StatusCfdiResponse import StatusCfdiResponse
class StatusCfdiRequest:
    @staticmethod
    def status(rfc_emisor, rfc_receptor, total, uuid, url, action):
        headers = {
            'Content-Type': "text/xml; charset=utf-8",
            'SOAPAction': action
        }
        body = """<?xml version="1.0" encoding="UTF-8"?>
         <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
           <tem:Consulta>
              <!--Optional:-->
              <tem:expresionImpresa><![CDATA[?re=""" + escape(rfc_emisor) + '&rr=' + escape(rfc_receptor) + '&tt=' + total + '&id=' + uuid + """]]></tem:expresionImpresa>
           </tem:Consulta>
        </soapenv:Body>
     </soapenv:Envelope>"""
        response = requests.request("POST", url, data = body.encode('utf-8'), headers = headers, verify = False, timeout = 300)
        return StatusCfdiResponse(response)