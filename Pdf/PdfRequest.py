from Pdf.PdfResponse import PdfResponse
from Utils.requestHelper import RequestHelper

class PdfRequest():
    @staticmethod
    def generate_pdf(urlApi, token, xml, b64Logo , template_id, extras):
        payload = {'xmlContent': xml,'logo': b64Logo, 'extras':extras, 'templateId':template_id}
        endpoint = urlApi + "/pdf/v1/api/GeneratePdf"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return PdfResponse(response)
    