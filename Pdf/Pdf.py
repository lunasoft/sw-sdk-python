from pdf.pdf_request import PdfRequest
from utils.services import Services

class Pdf(Services):
    def __init__(self, url, token, user = None, password = None):
        super(Pdf, self).__init__(url, token, user, password)
    
    def generate_pdf(self, xml, template_id = False):
        return PdfRequest.generate_pdf(self.get_url(), self.get_token(), xml, template_id)