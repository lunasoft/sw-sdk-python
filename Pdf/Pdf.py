from Pdf.PdfRequest import PdfRequest
from Utils.Services import Services

class Pdf(Services):
    urlApi = None
    def __init__(self, url, urlApi, token, user=None, password = None):
        super(Pdf, self).__init__(url, token, user, password)
        if urlApi:
            self.urlApi = urlApi
        else: 
            print("Debe especificar la urlApi")
    
    def generate_pdf(self,xml, b64Logo, template_id, extras):
        return PdfRequest.generate_pdf(self.urlApi, self.get_token(),xml, b64Logo, template_id, extras)

    def regenerate_pdf(self, uuid, b64Logo=None, template_id=None, extras=None):
        return PdfRequest.regenerate_pdf(self.urlApi, self.get_token(), uuid, b64Logo, template_id, extras)

    
