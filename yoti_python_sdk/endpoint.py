from deprecated import deprecated
import time
import uuid


class Endpoint(object):
    def __init__(self, sdk_id):
        self.sdk_id = sdk_id

    def get_activity_details_request_path(
        self, decrypted_request_token, no_params=False
    ):
        if no_params:
            return "/profile/{0}".format(decrypted_request_token)

        return "/profile/{0}?nonce={1}&timestamp={2}&appId={3}".format(
            decrypted_request_token,
            self.__create_nonce(),
            self.__create_timestamp(),
            self.sdk_id,
        )

    def get_aml_request_url(self, no_params=False):
        if no_params:
            return "/aml-check"

        return "/aml-check?appId={0}&timestamp={1}&nonce={2}".format(
            self.sdk_id, self.__create_timestamp(), self.__create_nonce()
        )

    def get_dynamic_share_request_url(self, no_params=False):
        if no_params:
            return "/qrcodes/app/{appid}".format(appid=self.sdk_id)

        return "/qrcodes/apps/{appid}?nonce={nonce}&timestamp={timestamp}".format(
            appid=self.sdk_id,
            nonce=self.__create_nonce(),
            timestamp=self.__create_timestamp(),
        )

    @staticmethod
    @deprecated
    def __create_nonce():
        return uuid.uuid4()

    @staticmethod
    @deprecated
    def __create_timestamp():
        return int(time.time() * 1000)
