import json
import traceback
from Utils.Response import Response
class RelationsResponse(Response):
    codStatus = None
    uuidConsultado = None
    resultado = None
    uuidsRelacionadosPadres = None
    uuidsRelacionadosHijos = None
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            if(bool(cResponse.text and cResponse.text.strip())):
                self.response = json.loads(cResponse.text)
                if(self.statusCode==200):
                    self.data = self.response["data"]
                    self.status = self.response["status"]
                    self.uuidConsultado = self.data["uuidConsultado"]
                    self.resultado = self.data["resultado"]
                    self.message = self.response["message"]
                    self.uuidsRelacionadosPadres = self.data["uuidsRelacionadosPadres"]
                    self.uuidsRelacionadosHijos = self.data["uuidsRelacionadosHijos"]
                else:
                    self.status = self.response["status"]
                    self.message = self.response["message"]
                    try:
                        self.messageDetail = self.response["messageDetail"]
                    except:
                        pass
            else:
                self.status = "error"
                self.message = cResponse.reason
                self.messageDetail = cResponse.request
        except:
            traceback.print_exc()

    def getCodStatus(self):
        return self.codStatus
    def getUuidConsultado(self):
        return self.uuidConsultado
    def getResultado(self):
        return self.resultado
    def getUuidsRelacionadosPadres(self):
        return self.uuidsRelacionadosPadres
    def getUuidsRelacionadosHijos(self):
        return self.uuidsRelacionadosHijos