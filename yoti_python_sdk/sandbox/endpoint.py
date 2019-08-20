from yoti_python_sdk.endpoint import Endpoint


class SandboxEndpoint(Endpoint):
    def __init__(self, sdk_id):
        super(SandboxEndpoint, self).__init__(sdk_id)

    def get_sandbox_path(self):
        return "/apps/{sdk_id}/tokens?timestamp={timestamp}&nonce={nonce}".format(
            sdk_id=self.sdk_id,
            nonce=self.__create_nonce(),
            timestamp=self.__create_timestamp(),
        )
