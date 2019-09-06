import json
import traceback
from Utils.response import Response

class AuthResponse(Response):
    token = None
    time_expire = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text, encoding='utf-8')
                if(self.status_code == 200):   
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                    self.token = self.data["token"]
                    self.time_expire = self.data["expires_in"]
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
    
    def get_token(self):
        return self.token

    def get_time_expire(self):
        return self.time_expire