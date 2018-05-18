import sys
from os import environ

from dotenv import load_dotenv
from os.path import join, dirname

from yoti_python_sdk import Client
from yoti_python_sdk import aml

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOTI_CLIENT_SDK_ID = environ.get('YOTI_CLIENT_SDK_ID')
YOTI_KEY_FILE_PATH = environ.get('YOTI_KEY_FILE_PATH')


# The following exits cleanly on Ctrl-C,
# while treating other exceptions as before.
def cli_exception(exception_type, value, tb):
    if not issubclass(exception_type, KeyboardInterrupt):
        sys.__excepthook__(exception_type, value, tb)


given_names = "Edward Richard George"
family_name = "Heath"

aml_address = aml.AmlAddress(country="GBR")
aml_profile = aml.AmlProfile(
    given_names,
    family_name,
    aml_address
)

if sys.stdin.isatty():
    sys.excepthook = cli_exception

client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)

aml_result = client.perform_aml_check(aml_profile)
print("AML Result for {0} {1}:".format(given_names, family_name))
print("On PEP list: " + str(aml_result.on_pep_list))
print("On fraud list: " + str(aml_result.on_fraud_list))
print("On watchlist: " + str(aml_result.on_watch_list))
