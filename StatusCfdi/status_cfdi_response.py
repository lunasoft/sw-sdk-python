import json
from utils.response import Response

class StatusCfdiResponse:
    status_code = None
    response = None
    codigoEstatus = None
    esCancelable = None
    estado = None
    estatusCancelacion = None
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            self.response = response.text
            self.codigoEstatus = self.search_codigoEstatus(self.response)
            self.esCancelable = self.search_esCancelable(self.response)
            self.estado = self.search_estado(self.response)
            self.estatusCancelacion = self.search_estatusCancelacion(self.response)
        except:
            self.statusCode = response.status_code
    def search_codigoEstatus(self, response):
        string = response.split("<a:CodigoEstatus>", 2)
        string2 = string[1].split("</a:CodigoEstatus>", 2)
        return string2[0]

    def search_esCancelable(self, response):
        string = response.split("<a:EsCancelable>", 2)
        string2 = string[1].split("</a:EsCancelable>", 2)
        return string2[0]

    def search_estado(self, response):
        string = response.split("<a:Estado>", 2)
        string2 = string[1].split("</a:Estado>", 2)
        return string2[0]

    def search_estatusCancelacion(self, response):
        string = response.split("<a:EstatusCancelacion>", 2)
        string2 = string[1].split("</a:EstatusCancelacion>", 2)
        return string2[0]