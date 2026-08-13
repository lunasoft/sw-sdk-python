from Pdf.PdfResponse import PdfResponse
from Pdf.RegeneratePdfResponse import RegeneratePdfResponse
from Utils.requestHelper import RequestHelper

class PdfRequest():
    @staticmethod
    def generate_pdf(urlApi, token, xml, b64Logo , template_id, extras):
        payload = {'xmlContent': xml,'logo': b64Logo, 'extras':extras, 'templateId':template_id}
        endpoint = urlApi + "/pdf/v1/api/GeneratePdf"
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return PdfResponse(response)

    @staticmethod
    def regenerate_pdf(urlApi, token, uuid, b64Logo=None, template_id=None, extras=None):
        """Regenera el PDF de un comprobante timbrado y lo reemplaza en el ADT.
        Todos los datos del cuerpo son opcionales: sólo se envían los informados.
        El formato del UUID no se valida en local, se envía tal cual y responde el servicio."""
        payload = {}
        if b64Logo is not None:
            payload['logo'] = b64Logo
        if template_id is not None:
            payload['templateId'] = template_id
        if extras is not None:
            payload['extras'] = extras
        endpoint = urlApi + "/pdf/v1/api/RegeneratePdf/" + str(uuid)
        response = RequestHelper.post_json_request(endpoint,token,payload)
        return RegeneratePdfResponse(response)
