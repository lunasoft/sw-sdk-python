from Utils.Services import Services
from Stamp.StampRequestV4 import StampRequestV4
from Utils.response_version import ResponseVersion

class StampV4(Services):
    def __init__(self, url, token=None, user=None, password=None):
        super(StampV4, self).__init__(url, token, user, password)

    def stamp(self, xml: str, headers: dict = None, version: ResponseVersion = ResponseVersion.V1):
        return StampRequestV4.stamp(
            url=self.get_url(),
            token=self.get_token(),
            xml=xml,
            headers=headers,
            version=version
        )
