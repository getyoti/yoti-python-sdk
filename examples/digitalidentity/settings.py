from os import environ
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

YOTI_CLIENT_SDK_ID = environ.get("YOTI_CLIENT_SDK_ID", None)
YOTI_KEY_FILE_PATH = environ.get("YOTI_KEY_FILE_PATH", None)
YOTI_API_URL = environ.get("YOTI_API_URL", "https://api.yoti.com/share")

if YOTI_CLIENT_SDK_ID is None or YOTI_KEY_FILE_PATH is None:
    raise ValueError("YOTI_CLIENT_SDK_ID or YOTI_KEY_FILE_PATH is None")

YOTI_APP_BASE_URL = environ.get("YOTI_APP_BASE_URL", "https://127.0.0.1:8000")
