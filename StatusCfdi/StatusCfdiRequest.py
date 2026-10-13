from xml.sax.saxutils import escape
from StatusCfdi.StatusCfdiResponse import StatusCfdiResponse
from Utils.requestHelper import RequestHelper

class StatusCfdiRequest:
    action = "http://tempuri.org/IConsultaCFDIService/Consulta"

    @staticmethod
    def status(url, rfc_emisor, rfc_receptor, total, uuid):
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
        response = RequestHelper.post_soap_request(url, StatusCfdiRequest.action, body)
        return StatusCfdiResponse(response)
