import json
import traceback
from Utils.Response import Response
class AcceptRejectResponse(Response):
    codStatus = None
    folios = None
    acuse = None
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            if(bool(cResponse.text and cResponse.text.strip())):
                self.response = json.loads(cResponse.text)
                if(self.statusCode==200):
                    self.data = self.response["data"]
                    self.acuse = self.data["acuse"]
                    self.status = self.response["status"]
                    self.codStatus = self.response["codStatus"]
                else:
                    self.message = self.response["message"]
                    self.messageDetail = self.response["messageDetail"]
                    self.status = self.response["status"]
            else:
                self.status = "error"
                self.message = cResponse.reason
                self.messageDetail = cResponse.request
        except:
            traceback.print_exc()

    def getCodStatus(self):
        return self.codStatus
    def getFolios(self):
        return self.folios
    def getAcuse(self):
        return self.acuse