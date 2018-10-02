from Pdf.PdfRequest import PdfRequest
from Utils.Services import Services

class Pdf(Services):
    def __init__(self, url, token, user=None, password=None):
        super(Pdf,self).__init__(url, token, user, password)
    
    def generatePdf(self,xml,templateId=False):
        return PdfRequest.generatePdf(self.url, self.token, xml, templateId)