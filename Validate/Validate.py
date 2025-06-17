from Validate.ValidateRequest import ValidateRequest
from Utils.Services import Services

class Validate(Services):
    def __init__(self, url, token = None, user = None, password = None):
        super(Validate,self).__init__(url, token, user, password)

    def ValidateXml(self, xml,status=None):
        return ValidateRequest.validate_xml(self.get_url(), self.get_token(), xml,status)