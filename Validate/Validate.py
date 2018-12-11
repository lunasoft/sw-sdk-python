from validate.validate_request import ValidateRequest
from utils.services import Services

class Validate(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Validate, self).__init__(url, token, user, password)

    def validate_lrfc(self, lrfc):
        return ValidateRequest.validate_lrfc(self.get_url(), self.get_token(), lrfc)

    def validate_lco(self, lco):
        return ValidateRequest.validate_lco(self.get_url(), self.get_token(), lco)

    def validate_xml(self, xml):
        return ValidateRequest.validate_xml(self.get_url(), self.get_token(), xml)