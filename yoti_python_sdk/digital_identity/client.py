import yoti_python_sdk

import json, base64

from yoti_python_sdk.http import SignedRequest

from .create_share_session_result import CreateShareSessionResult
from .get_share_session_result import GetShareSessionResult
from .create_share_qr_code_result import CreateShareQrCodeResult
from .get_share_qr_code_result import GetShareQrCodeResult
from .get_share_receipt_result import GetShareReceiptResult

from .receipts.receipt_response import ReceiptResponse
from .receipts.receipt_item_key_response import ReceiptItemKeyResponse

from .receipts.crypto.decryption import build_user_content_from_encrypted_content, unwrap_receipt_key

class DigitalIdentityClient(object):
    """
    Client used for communication with the Yoti Doc Scan service where any
    signed request is required
    """
    def __init__(self, sdk_id, key, api_url=None):
        self.__sdk_id = sdk_id
        self.__key = key
        if api_url is not None:
            self.__api_url = api_url
        else:
            self.__api_url = yoti_python_sdk.YOTI_DOC_SCAN_API_URL
    def create_share_session(self, share_session_config):
        """
        Creates a share session
    
        :param share_session_config: the share session config
        :type share_session_config: dict
        :return: the create share session result
        :rtype: CreateShareSessionResult
        """
    
    
        payload = json.dumps(share_session_config).encode("utf-8")
        
        request = (
            SignedRequest.builder()
            .with_base_url(self.__api_url)
            .with_header("Content-Type", "application/json")
            .with_header("X-Yoti-Auth-Id", self.__sdk_id)
            .with_pem_file(self.__key)
            .with_endpoint("/v2/sessions")
            .with_param("appId", self.__sdk_id)
            .with_post()
            .with_payload(payload)
            .build()
        )
    
        response = request.execute()
    
        #if response.status_code != 201:
        #    raise Exception("Failed to create session", response)
    
        if response.status_code != 201:
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            raise Exception("Failed to create session", response)
        
        data = json.loads(response.text)
    
        return CreateShareSessionResult(data)
    
    def get_share_session(self, session_id):
        """
        Retrieves a share session
    
        :param session_id: the session id
        :type session_id: str
        :return: the get share session result
        :rtype: GetShareSessionResult
        """
    
        request = (
            SignedRequest.builder()
            .with_base_url(self.__api_url)
            .with_header("X-Yoti-Auth-Id", self.__sdk_id)
            .with_pem_file(self.__key)
            .with_endpoint("/v2/sessions/{}".format(session_id))
            .with_param("appId", self.__sdk_id)
            .with_get()
            .build()
        )
    
        response = request.execute()
    
        if response.status_code != 200:
            raise Exception("Failed to get session", response)
        
        data = json.loads(response.text)
    
        return GetShareSessionResult(data)
    
    def create_share_qr_code(self,session_id):
        """
        Creates a share QR code
    
        :param session_id: the session id
        :type session_id: str
        :return: the share QR code result
        :rtype: CreateShareQrCodeResult
        """
    
        #Create an empty payload
        payload = json.dumps({}).encode("utf-8")
    
        request = (
            SignedRequest.builder()
            .with_base_url(self.__api_url)
            .with_header("Content-Type", "application/json")
            .with_header("X-Yoti-Auth-Id", self.__sdk_id)
            .with_pem_file(self.__key)
            .with_endpoint("/v2/sessions/{}/qr-codes".format(session_id))
            .with_param("appId", self.__sdk_id)
            .with_post()
            .with_payload(payload)
            .build()
        )
        
        response = request.execute()
    
        if response.status_code != 201:
            raise Exception("Failed to create qr code", response)
        
        data = json.loads(response.text)
    
        return CreateShareQrCodeResult(data)
    
    def get_share_qr_code(self,qrCodeId):
        """
        Retrieves a share QR code
    
        :param qrCodeId: the qr code id
        :type qrCodeId: str
        :return: the get share QR code result
        :rtype: GetShareQrCodeResult
        """
    
        request = (
            SignedRequest.builder()
            .with_base_url(self.__api_url)
            .with_header("X-Yoti-Auth-Id", self.__sdk_id)
            .with_pem_file(self.__key)
            .with_endpoint("/v2/qr-codes/{}".format(qrCodeId))
            .with_param("appId", self.__sdk_id)
            .with_get()
            .build()
        )
    
        response = request.execute()
    
        if response.status_code != 200:
            raise Exception("Failed to get session", response)
        
        data = json.loads(response.text)
    
        return GetShareQrCodeResult(data)
    
    def fetch_receipt(self, receiptId):
        """
        Fetches the receipt
    
        :param receiptId: the receipt id
        :type receiptId: str
        :return: the receipt response
        :rtype: ReceiptResponse
        """
        
        # Convert the receipt id to a url safe base64 string
        receiptIdUrl = base64.urlsafe_b64encode(base64.b64decode(receiptId)).decode()
      
        
        request = (
            SignedRequest.builder()
            .with_base_url(self.__api_url)
            .with_header("X-Yoti-Auth-Id", self.__sdk_id)
            .with_pem_file(self.__key)
            .with_endpoint("/v2/receipts/{}".format(receiptIdUrl))
            .with_param("appId", self.__sdk_id)
            .with_get()
            .build()
        )
    
        response = request.execute()
    
        if response.status_code != 200:
            raise Exception("Failed to get session", response)
        
        data = json.loads(response.text)
        
        return ReceiptResponse(data)
    
    def fetch_receipt_item_key(self, receiptItemKeyId):
        """
        Fetches the receipt item key
    
        :param receiptItemKeyId: the receipt item key id
        :type receiptItemKeyId: str
        :return: the receipt item key response
        :rtype: ReceiptItemKeyResponse
        """ 
        
        request = (
            SignedRequest.builder()
            .with_base_url(self.__api_url)
            .with_header("X-Yoti-Auth-Id", self.__sdk_id)
            .with_pem_file(self.__key)
            .with_endpoint("/v2/wrapped-item-keys/{}".format(receiptItemKeyId))
            .with_param("appId", self.__sdk_id)
            .with_get()
            .build()
        )
    
        response = request.execute()
    
        if response.status_code != 200:
            raise Exception("Failed to get session", response)
        
        data = json.loads(response.text)
    
        return ReceiptItemKeyResponse(data)
    
    def get_share_receipt(self, receiptId):
        """
        Retrieves a share receipt
    
        :param receiptId: the receipt id
        :type receiptId: str
        :return: the get share receipt result
        :rtype: GetShareReceiptResult
        """
           
        receipt_response = self.fetch_receipt(receiptId)
        item_key_id = receipt_response.wrappedItemKeyId
    
        if (item_key_id is None):
            return GetShareReceiptResult(receipt_response)
        
        encrypted_item_key_response = self.fetch_receipt_item_key(item_key_id)
    
        receipt_content_key = unwrap_receipt_key(
            receipt_response.wrappedKey,
            encrypted_item_key_response.value,
            encrypted_item_key_response.iv,
            self.__key
        )
    
        user_content = build_user_content_from_encrypted_content(
            receipt_response.otherPartyContent,
            receipt_content_key,
        )
        
        return GetShareReceiptResult(receipt_response, user_content)
