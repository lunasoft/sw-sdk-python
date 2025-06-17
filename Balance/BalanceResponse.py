import json
import traceback
from Utils.response import Response

class AccountBalanceResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if bool(response.text and response.text.strip()):
                self.response = json.loads(response.text.encode().decode("utf8"))
                if self.status_code == 200:
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                else:
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    if "messageDetail" in self.response:
                        self.messageDetail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except Exception:
            traceback.print_exc()

class BalanceResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.status_code == 200):
                    self.data = Data(self.response["data"])
                    self.status = self.response["status"]
                else:
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
            
class Data:
    def __init__(self, data):
        self.idUserBalance = data.get("idUserBalance", "")
        self.idUser = data.get("idUser", "")
        self.stampsBalance = data.get("stampsBalance", 0)
        self.stampsUsed = data.get("stampsUsed", 0)
        self.stampsAssigned = data.get("stampsAssigned", 0)
        self.unlimited = data.get("unlimited", False)
        self.expirationDate = data.get("expirationDate", "")
        self.lastTransaction = LastTransaction(data["lastTransaction"]) if "lastTransaction" in data else None

class LastTransaction:
    def __init__(self, transaction):
        self.folio = transaction.get("folio", 0)
        self.idUSer = transaction.get("idUSer", "")
        self.idUserReceiver = transaction.get("idUserReceiver", "")
        self.nameReceiver = transaction.get("nameReceiver", "")
        self.stampsIn = transaction.get("stampsIn", 0)
        self.stampsOut = transaction.get("stampsOut", None)
        self.stampsCurrent = transaction.get("stampsCurrent", 0)
        self.comment = transaction.get("comment", "")
        self.date = transaction.get("date", "")
        self.isEmailSent = transaction.get("isEmailSent", False)