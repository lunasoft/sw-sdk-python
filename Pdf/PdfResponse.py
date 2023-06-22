import json
import traceback
from Utils.response import Response

class PdfResponse(Response):
    contentB64 = None
    contentSizeBytes = None
    uuid = None
    serie = None
    folio = None
    stampDate = None
    issuedDate = None
    rfcIssuer = None
    rfcReceptor = None
    total = None
    def __init__(self, response):
        try:
            self.statusCode = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.statusCode == 200):
                    try:
                        self.data = self.response["data"]
                        self.status = self.response["status"]
                        self.contentB64 = self.data['contentB64']
                        self.contentSizeBytes = self.data['contentSizeBytes']
                        self.uuid = self.data['uuid']
                        self.serie = self.data['serie']
                        self.folio = self.data['folio']
                        self.stampDate = self.data['stampDate']
                        self.issuedDate = self.data['issuedDate']
                        self.rfcIssuer = self.data['rfcIssuer']
                        self.rfcReceptor = self.data['rfcReceptor']
                        self.total = self.data['total']
                    except:
                        self.status = self.response["status"]
                else:
                    self.message = self.response["message"]
                    if "messageDetail" in self.response: 
                        self.messageDetail = self.response["messageDetail"]
                    self.status = self.response["status"] 
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()
    
    def get_content_b64(self):
        return self.contentB64
    
    def get_content_size_bytes(self):
        return self.contentSizeBytes
    
    def get_uuid(self):
        return self.uuid
    
    def get_serie(self):
        return self.serie
    
    def get_folio(self):
        return self.folio
    
    def get_stamp_date(self):
        return self.stampDate
    
    def get_issued_date(self):
        return self.issuedDate
    
    def get_rfc_issuer(self):
        return self.rfcIssuer
    
    def get_rfc_receptor(self):
        return self.rfcReceptor
    
    def get_total(self):
        return self.total
            