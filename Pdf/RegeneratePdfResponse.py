import json
import traceback
from Utils.response import Response

#La regeneración de PDF sólo regresa un mensaje: la respuesta no trae las llaves
#status ni data, por eso no puede reutilizar PdfResponse.
class RegeneratePdfResponse(Response):
    def __init__(self, response):
        try:
            self.status_code = response.status_code
            self.status = "success" if self.status_code == 200 else "error"
            if(bool(response.text and response.text.strip())):
                try:
                    self.response = json.loads(response.text.encode().decode('utf8'))
                    if "message" in self.response:
                        self.message = self.response["message"]
                    if "messageDetail" in self.response:
                        self.messageDetail = self.response["messageDetail"]
                except ValueError:
                    #Un cuerpo que no es JSON se conserva tal cual en message.
                    self.message = response.text
            else:
                self.message = response.reason
        except:
            traceback.print_exc()
