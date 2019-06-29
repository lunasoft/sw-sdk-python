import json
import traceback
from Utils.response import Response
class RelationsResponse(Response):
    codStatus = None
    uuid_consultado = None
    resultado = None
    uuids_relacionados_padres = None
    uuids_relacionados_hijos = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            if(bool(response.text and response.text.strip())):
                self.response = json.loads(response.text, encoding='utf-8')
                if(self.status_code == 200):
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    if(self.response["codStatus"] == "2000"):
                        self.uuid_consultado = self.data["uuidConsultado"]
                        self.resultado = self.data["resultado"]
                        self.uuids_relacionados_padres = self.data["uuidsRelacionadosPadres"]
                        self.uuids_relacionados_hijos = self.data["uuidsRelacionadosHijos"]
                else:
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    try:
                        self.messageDetail = self.response["messageDetail"]
                    except:
                        pass
            else:
                self.status = "error"
                self.message = response.reason
                self.messageDetail = response.request
        except:
            traceback.print_exc()

    def get_codStatus(self):
        return self.codStatus
    def get_uuid_consultado(self):
        return self.uuid_consultado
    def get_resultado(self):
        return self.resultado
    def get_uuids_relacionados_padres(self):
        return self.uuids_relacionados_padres
    def get_uuids_relacionados_hijos(self):
        return self.uuids_relacionados_hijos