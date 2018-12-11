import json
import traceback
from utils.response import Response
class CancelationResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text)
                if(self.status_code == 200):
                    self.status = self.response["status"]
                    self.data = self.response["data"]
                else:
                    self.message = self.response["message"]
                    self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()