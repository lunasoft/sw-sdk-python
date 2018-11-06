import requests
from StatusCfdi.StatusCfdiResponse import StatusCfdiResponse
class StatusCfdiRequest:
    @staticmethod
    def status(cRFCEmisor, cRFCReceptor, cTotal, cUUID, cURL, cAction):
        headers = {
            'Content-Type': "text/xml; charset=utf-8",
            'SOAPAction': cAction
        }
        body = """<?xml version="1.0" encoding="UTF-8"?>
         <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
           <tem:Consulta>
              <!--Optional:-->
              <tem:expresionImpresa><![CDATA[?re="""+cRFCEmisor.replace("&", "&amp;")+'&rr='+cRFCReceptor.replace("&", "&amp;")+'&tt='+cTotal+'&id='+cUUID+"""]]></tem:expresionImpresa>
           </tem:Consulta>
        </soapenv:Body>
     </soapenv:Envelope>"""
        response = requests.request("POST", cURL + "?wsdl", data=body,headers=headers, verify = False, timeout = 300)
        return StatusCfdiResponse(response)