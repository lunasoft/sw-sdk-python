import json
import traceback
from Utils.response import Response

class PdfResponse(Response):
    content_b64 = None
    content_size_bytes = None
    uuid = None
    serie = None
    folio = None
    stamp_date = None
    issued_date = None
    rfc_issuer = None
    rfc_receptor = None
    total = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.status_code == 200):
                    try:
                        self.data = self.response["data"]
                        self.status = self.response["status"]
                        self.content_b64 = self.data['contentB64']
                        self.content_size_bytes = self.data['contentSizeBytes']
                        self.uuid = self.data['uuid']
                        self.serie = self.data['serie']
                        self.folio = self.data['folio']
                        self.stamp_date = self.data['stampDate']
                        self.issued_date = self.data['issuedDate']
                        self.rfc_issuer = self.data['rfcIssuer']
                        self.rfc_receptor = self.data['rfcReceptor']
                        self.total = self.data['total']
                    except:
                        self.status = self.response["status"]
                else:
                    self.message = self.response["message"]
                    if "messageDetail" in self.response: 
                        self.message_detail = self.response["messageDetail"]
                    self.status = self.response["status"] 
            else:
                self.status = "error"
                self.message = response.reason
                self.message_detail = response.request
        except:
            traceback.print_exc()
    
    def get_content_b64(self):
        return self.content_b64
    
    def get_content_size_bytes(self):
        return self.content_size_bytes
    
    def get_uuid(self):
        return self.uuid
    
    def get_serie(self):
        return self.serie
    
    def get_folio(self):
        return self.folio
    
    def get_stamp_date(self):
        return self.stamp_date
    
    def get_issued_date(self):
        return self.issued_date
    
    def get_rfc_issuer(self):
        return self.rfc_issuer
    
    def get_rfc_receptor(self):
        return self.rfc_receptor
    
    def get_total(self):
        return self.total
            