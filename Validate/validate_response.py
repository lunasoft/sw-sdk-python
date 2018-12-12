import json
import traceback
from Utils.response import Response

class ValidateResponse(Response):
    def __init__(self, response):
        try:
            self.statusCode = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text)
                if(self.statusCode == 200):
                    try:
                        self.data = self.response["data"]
                        self.status = self.response["status"]
                    except:
                        self.status = self.response["status"]
                else:
                    self.message = self.response["message"]
                    self.messageDetail = self.response["messageDetail"]
                    self.status = self.response["status"] 
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()