from Validate.ValidateRequest import ValidateRequest
from Utils.Services import Services

class Validate(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Validate,self).__init__(url, token, user, password)

    def ValidateLrfc(self, lrfc):
        return ValidateRequest.validate_lrfc(self.url, self.token, lrfc)

    def ValidateLco(self, lco):
        return ValidateRequest.validate_lco(self.url, self.token, lco)

    def ValidateXml(self, xml):
        return ValidateRequest.validate_xml(self.url, self.token, xml)