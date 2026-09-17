import json
import traceback
from Utils.response import Response
class AcceptRejectResponse(Response):
    cod_status = None
    folios = None
    acuse = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text)
                if(self.status_code == 200):
                    self.data = self.response["data"]
                    self.acuse = self.data["acuse"]
                    self.status = self.response["status"]
                    self.cod_status = self.response["codStatus"]
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

    def get_cod_status(self):
        return self.cod_status
    def get_folios(self):
        return self.folios
    def get_acuse(self):
        return self.acuse