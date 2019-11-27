class Endpoint(object):
    def __init__(self, sdk_id):
        self.sdk_id = sdk_id

    @staticmethod
    def get_activity_details_request_path(decrypted_request_token):
        return "/profile/{0}".format(decrypted_request_token)

    @staticmethod
    def get_aml_request_url():
        return "/aml-check"

    def get_dynamic_share_request_url(self):
        return "/qrcodes/apps/{appid}".format(appid=self.sdk_id)
