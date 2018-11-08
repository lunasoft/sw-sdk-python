import json
import traceback
from Utils.Response import Response

class AuthResponse(Response):
    token = None
    timeExpire = None
    def __init__(self,cResponse):
        try:
            self.statusCode = cResponse.status_code
            if(bool(cResponse.text and cResponse.text.strip())):
                self.response = json.loads(cResponse.text)
                if(self.statusCode==200):   
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                    self.token = self.data["token"]
                    self.timeExpire = self.data["expires_in"]
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
    
    def getToken(self):
        return self.token

    def getTimeExpire(self):
        return self.timeExpire