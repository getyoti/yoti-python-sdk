from yoti_python_sdk.endpoint import Endpoint
from yoti_python_sdk.utils import create_timestamp, create_nonce


class SandboxEndpoint(Endpoint):
    def __init__(self, sdk_id):
        super(SandboxEndpoint, self).__init__(sdk_id)

    def get_sandbox_path(self):
        return "/apps/{sdk_id}/tokens?timestamp={timestamp}&nonce={nonce}".format(
            sdk_id=self.sdk_id, nonce=create_nonce(), timestamp=create_timestamp()
        )
