import json
import traceback
from Utils.response import Response

class AccountUserResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if bool(response.text and response.text.strip()):
                self.response = json.loads(response.text.encode().decode("utf8"))
                if self.status_code == 200:
                    if isinstance(self.response["data"], dict):
                        self.data = DataItem(self.response["data"])
                    elif isinstance(self.response["data"], list):
                        self.data = DataList(self.response["data"])
                    elif isinstance(self.response["data"], str):
                        self.data = self.response["data"]
                    self.status = self.response["status"]
                else:
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    if "messageDetail" in self.response:
                        self.messageDetail = self.response["messageDetail"]
            elif self.status_code == 204:
                    self.status = "success"
                    self.status_code = 200
                    self.data = "Usuario Eliminado con exito"
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except Exception:
            traceback.print_exc()
            
class DataItem:
    def __init__(self, data):
        self.idUser = data.get("idUser", "")
        self.idDealer = data.get("idDealer", "")
        self.name = data.get("name", "")
        self.taxId = data.get("taxId", "")
        self.username = data.get("username", "")
        self.lastPasswordChange = data.get("lastPasswordChange", "")
        self.email = data.get("email", "")
        self.notificationEmail = data.get("notificationEmail", "")
        self.profile = data.get("profile", 0)
        self.isActive = data.get("isActive", False)
        self.registeredDate = data.get("registeredDate", "")
        self.accessToken = data.get("accessToken", "")
        self.stamps = data.get("stamps", 0)
        self.phone = data.get("phone", "")
        self.isUnlimited = data.get("isUnlimited", False)

class DataList:
    def __init__(self, data):
        self.items = [DataItem(item) for item in data] 