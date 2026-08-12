import json
import traceback
from Utils.response import Response
class StorageResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.status_code == 200):
                    self.status = self.response["status"]
                    self.data = self.response["data"]
                else:
                    if "status" in self.response:
                        self.status = self.response["status"]
                    self.message = self.response["message"]
                    if "messageDetail" in self.response:
                        self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()

    #Un UUID sin coincidencias regresa una lista vacía, no es un error.
    def get_records(self):
        if self.data:
            return self.data.get("records") or []
        return []

    def get_metadata(self):
        if self.data:
            return self.data.get("metaData")
        return None

    def get_first_record(self):
        records = self.get_records()
        if records:
            return records[0]
        return None

    def get_url_xml(self):
        record = self.get_first_record()
        if record:
            return record.get("urlXml")
        return None

    #La documentación oficial nombra el campo urlPDF y el SDK de .NET urlPdf.
    def get_url_pdf(self):
        record = self.get_first_record()
        if record:
            return record.get("urlPdf") or record.get("urlPDF")
        return None
