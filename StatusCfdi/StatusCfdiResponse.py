import json
from Utils.Response import Response

class StatusCfdiResponse:
    statusCode = None
    response = None
    codigoEstatus = None
    esCancelable = None
    estado = None
    estatusCancelacion = None
    def __init__(self, cResponse):
        try:
            self.statusCode = cResponse.status_code
            self.response = cResponse.text
            self.codigoEstatus = self.searchCodigoEstatus(self.response)
            self.esCancelable = self.searchEsCancelable(self.response)
            self.estado = self.searchEstado(self.response)
            self.EstatusCancelacion = self.searchEstatusCancelacion(self.response)
        except:
            self.statusCode = cResponse.status_code
    def searchCodigoEstatus(self, cResponse):
        string = cResponse.split("<a:CodigoEstatus>", 2)
        string2 = string[1].split("</a:CodigoEstatus>", 2)
        return string2[0]

    def searchEsCancelable(self, cResponse):
        string = cResponse.split("<a:EsCancelable>",2)
        string2 = string[1].split("</a:EsCancelable>", 2)
        return string2[0]

    def searchEstado(self, cResponse):
        string = cResponse.split("<a:Estado>", 2)
        string2 = string[1].split("</a:Estado>", 2)
        return string2[0]

    def searchEstatusCancelacion(self, cResponse):
        string = cResponse.split("<a:EstatusCancelacion>", 2)
        string2 = string[1].split("</a:EstatusCancelacion>", 2)
        return string2[0]