from Pdf.PdfRequest import PdfRequest
from Utils.Services import Services

class Pdf(Services):
    url_api = None
    def __init__(self, url, url_api, token, user=None, password = None):
        super(Pdf, self).__init__(url, token, user, password)
        if url_api:
            self.url_api = url_api
        else: 
            print("Debe especificar la url_api")
    
    def generate_pdf(self,xml, b64Logo, template_id, extras):
        return PdfRequest.generate_pdf(self.url_api, self.get_token(),xml, b64Logo, template_id, extras)

    def regenerate_pdf(self, uuid, b64Logo=None, template_id=None, extras=None):
        return PdfRequest.regenerate_pdf(self.url_api, self.get_token(), uuid, b64Logo, template_id, extras)

    
