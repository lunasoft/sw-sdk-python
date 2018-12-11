import json
import traceback
from Utils.response import Response

class StampResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text)
                if(self.status_code == 200):
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                else:
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()