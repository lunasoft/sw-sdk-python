from Pdf.PdfRequest import PdfRequest
from Utils.Services import Service

class Pdf(Service):
    def __init__(self, url, urlApi, token, user=None, password = None):
        super(Pdf, self).__init__(url,urlApi,token, user, password)
    
    def generate_pdf(self,xml, b64Logo, template_id, extras):
        return PdfRequest.generate_pdf(self.get_urlApi(), self.get_token(),xml, b64Logo, template_id, extras)
    
    
