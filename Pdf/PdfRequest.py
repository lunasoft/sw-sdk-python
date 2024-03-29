import requests
import json
from Pdf.PdfResponse import PdfResponse

class PdfRequest():
    @staticmethod
    def generate_pdf(urlApi, token, xml, b64Logo , template_id, extras):
        headers = {
            'Authorization': "Bearer " + token,
            'Content-Type': "application/json"
        }
        payload = {'xmlContent': xml,'logo': b64Logo, 'extras':extras, 'templateId':template_id}
        response = requests.request("POST", urlApi + "/pdf/v1/api/GeneratePdf", data = json.dumps(payload), headers = headers)
        return PdfResponse(response)
    