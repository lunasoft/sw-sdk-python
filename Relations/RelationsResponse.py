import json
import traceback
from Utils.response import Response
class RelationsResponse(Response):
    cod_status = None
    queried_uuid = None
    result = None
    parent_related_uuids = None
    child_related_uuids = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text.encode().decode('utf8'))
                if(self.status_code == 200):
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    if(self.response["codStatus"] == "2000"):
                        self.queried_uuid = self.data["uuidConsultado"]
                        self.result = self.data["resultado"]
                        self.parent_related_uuids = self.data["uuidsRelacionadosPadres"]
                        self.child_related_uuids = self.data["uuidsRelacionadosHijos"]
                else:
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    if "messageDetail" in self.response: 
                        self.message_detail = self.response["messageDetail"]
            else:
                self.status = "error"
                self.message = response.reason
                self.message_detail = response.request
        except:
            traceback.print_exc()

    def get_cod_status(self):
        return self.cod_status
    def get_queried_uuid(self):
        return self.queried_uuid
    def get_result(self):
        return self.result
    def get_parent_related_uuids(self):
        return self.parent_related_uuids
    def get_child_related_uuids(self):
        return self.child_related_uuids