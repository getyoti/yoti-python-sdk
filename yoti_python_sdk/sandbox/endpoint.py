from yoti_python_sdk.endpoint import Endpoint
import time
import uuid


class SandboxEndpoint(Endpoint):
    def __init__(self, sdk_id):
        super(SandboxEndpoint, self).__init__(sdk_id)

    def get_sandbox_path(self):
        return "/apps/{sdk_id}/tokens?timestamp={timestamp}&nonce={nonce}".format(
            sdk_id=self.sdk_id,
            nonce=self.__create_nonce(),
            timestamp=self.__create_timestamp(),
        )

    @staticmethod
    def __create_nonce():
        return uuid.uuid4()

    @staticmethod
    def __create_timestamp():
        return int(time.time() * 1000)
