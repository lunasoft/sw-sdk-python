import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utils.Response import Response

class AuthResponse(Response):
    def __init__(self,cResponse):
        try:
            self.response = json.loads(cResponse.text)
            self.data = self.response["data"]
            self.status = self.response["status"]
            self.token = self.data["token"]
            self.timeExpire = self.data["expires_in"]
        except:
            self.message = self.response["message"]
            self.messageDetail = self.response["messageDetail"]
            self.status = self.response["status"]
    
    def getToken(self):
        return self.token

    def getTimeExpire(self):
        return self.timeExpire