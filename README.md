# Yoti Python SDK #

Welcome to the Yoti Python SDK. This repo contains the tools and step by step instructions you need to quickly integrate your Python back-end with Yoti so that your users can share their identity details with your application in a secure and trusted way.

## Table of Contents

1) [An Architectural view](#an-architectural-view) -
High level overview of integration

1) [References](#references) -
Guides before you start

1) [Requirements](#requirements) -
Everything you need to get started

1) [Installing the SDK](#installing-the-sdk) -
How to install our SDK

1) [SDK Project import](#sdk-project-import) -
How to install the SDK to your project

1) [Configuration](#configuration) -
Entry point explanation

1) [Handling Users](#handling-users) -
How to manage users

1) [AML Integration](#aml-integration) -
How to integrate with Yoti's AML (Anti Money Laundering) service

1) [Running the examples](#running-the-examples) -
How to retrieve a Yoti profile using the token

1) [Running the tests](#running-the-tests) -
Running tests for SDK example

1) [API Coverage](#api-coverage) -
Attributes defined

1) [Support](#support) -
Please feel free to reach out

## An Architectural View

Before you start your integration, here is a bit of background on how the integration works. To integrate your application with Yoti, your back-end must expose a GET endpoint that Yoti will use to forward tokens.
The endpoint can be configured in the Yoti Dashboard when you create/update your application. For more information on how to create an application please check our [developer page](https://www.yoti.com/developers/documentation/#login-button-setup).

The image below shows how your application back-end and Yoti integrate into the context of a Login flow.
Yoti SDK carries out for you steps 6, 7 and the profile decryption in step 8.

![alt text](login_flow.png "Login flow")

Yoti also allows you to enable user details verification from your mobile app by means of the Android (TBA) and iOS (TBA) SDKs. In that scenario, your Yoti-enabled mobile app is playing both the role of the browser and the Yoti app. Your back-end doesn't need to handle these cases in a significantly different way. You might just decide to handle the `User-Agent` header in order to provide different responses for desktop and mobile clients.

## References

* [AES-256 symmetric encryption][]
* [RSA pkcs asymmetric encryption][]
* [Protocol buffers][]
* [Base64 data][]

[AES-256 symmetric encryption]:   https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
[RSA pkcs asymmetric encryption]: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
[Protocol buffers]:               https://en.wikipedia.org/wiki/Protocol_Buffers
[Base64 data]:                    https://en.wikipedia.org/wiki/Base64

## Requirements

To see the versions of Python this SDK is compatible with, see the [.travis.yml](/.travis.yml) file.

## Installing the SDK

To import the Yoti SDK inside your project, simply run the following command from your terminal:

```shell
pip install yoti
```

## SDK Project Import

You can reference the project URL by adding the following import:

```python
import yoti_python_sdk
```

## Configuration

After creating your application on the [Yoti Dashboard](https://www.yoti.com/dashboard/), you need to download the `.PEM` key and save it *outside* the repo (keep it private).

The variables required for the SDK to work are found in the tabs on your Yoti application's settings page ([Yoti Dashboard](https://www.yoti.com/dashboard/)). These are:

* **`YOTI_SCENARIO_ID`** - This is used to configure the [Yoti Login Button](https://www.yoti.com/developers/documentation/#2-front-end-integration).
* **`YOTI_CLIENT_SDK_ID`** - This is the SDK identifier generated by Yoti Dashboard in the Key tab when you create your app. Note this is not your Application Identifier which is needed by your client-side code.
* **`YOTI_KEY_FILE_PATH`** - This is the path to the application .pem file, we recommend keeping your .pem file outside of your repository. It can be downloaded only once from the Keys tab in your Yoti Dashboard. (e.g. /home/user/.ssh/access-security.pem).

**Please do not open the pem file** as this might corrupt the key and you will need to create a new application.

One way to configure these environment variables is to use an .env file. There are `.env.example` files supplied in the [Django](/examples/yoti_example_django/yoti_example/.env.example) and [Flask](/examples/yoti_example_flask/.env.example) example projects, which you can rename to `.env` and enter your settings into this file. **Do not use quotes when entering your environment variables**

### Example Initialisation

```python
from yoti_python_sdk import Client
@app.route('/profile')
def auth():
    client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    activity_details = client.get_activity_details(request.args['token'])
```

## Handling Users

When you retrieve the user profile, you receive a user ID generated by Yoti exclusively for your application.
This means that if the same individual logs into another app, Yoti will assign her/him a different ID.
You can use this ID to verify whether (for your application) the retrieved profile identifies a new or an existing user.
Here is an example of how this works:

```python
client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
activity_details = client.get_activity_details(token)

profile = activity_details.profile
        
selfie = profile.selfie.value
given_names = profile.given_names.value
family_name = profile.family_name.value
full_name = profile.full_name.value
phone_number = profile.phone_number.value
date_of_birth = profile.date_of_birth.value
postal_address = profile.postal_address.value
gender = profile.gender.value
nationality = profile.nationality.value
email_address = profile.email_address.value
        
remember_me_id = activity_details.user_id
parent_remember_me_id = activity_details.parent_remember_me_id
receipt_id = activity_details.receipt_id
timestamp = activity_details.timestamp
base64_selfie_uri = activity_details.base64_selfie_uri
```

You can retrieve the anchors, sources and verifiers for each attribute as follows:
```python
given_names_attribute = profile.given_names

given_names_anchors = given_names_attribute.anchors
given_names_sources = given_names_attribute.sources
given_names_verifiers = given_names_attribute.verifiers
```

You can also retrieve further properties from these respective anchors in the following way:
```python
source_anchor = given_names_sources[0]
value = source_anchor.value
sub_type = source_anchor.sub_type
timestamp = source_anchor.signed_timestamp
origin_server_certs = source_anchor.origin_server_certs
```

If you have chosen `Verify Condition` on the [Yoti Dashboard](https://www.yoti.com/dashboard/applications) with the age condition of "Over 18", you can retrieve the user information as follows:
```python
age_verification_attribute = profile.get_attribute("age_over:18")
```
You can retrieve the sources and verifiers in the same way as detailed above.

## AML Integration

Yoti provides an AML (Anti Money Laundering) check service to allow a deeper KYC process to prevent fraud. This is a chargeable service, so please contact [sdksupport@yoti.com](mailto:sdksupport@yoti.com) for more information.

Yoti will provide a boolean result on the following checks:

* PEP list - Verify against Politically Exposed Persons list
* Fraud list - Verify against  US Social Security Administration Fraud (SSN Fraud) list
* Watch list - Verify against watch lists from the Office of Foreign Assets Control

To use this functionality you must ensure your application is assigned to your Organisation in the Yoti Dashboard - please see [here](https://www.yoti.com/developers/documentation/#1-creating-an-organisation) for further information.

For the AML check you will need to provide the following:

* Data provided by Yoti (please ensure you have selected the Given name(s) and Family name attributes from the Data tab in the Yoti Dashboard)
  * Given name(s)
  * Family name
* Data that must be collected from the user:
  * Country of residence (must be an ISO 3166 3-letter code)
  * Social Security Number (US citizens only)
  * Postcode/Zip code (US citizens only)

### Consent

Performing an AML check on a person *requires* their consent.
**You must ensure you have user consent *before* using this service.**

### Code Example

Given a YotiClient initialised with your SDK ID and KeyPair (see [Client Initialisation](#client-initialisation)) performing an AML check is a straightforward case of providing basic profile data.

```python
from yoti_python_sdk import aml
from yoti_python_sdk import Client

client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
given_names = "Edward Richard George"
family_name = "Heath"

aml_address = aml.AmlAddress(country="GBR")
aml_profile = aml.AmlProfile(
    given_names,
    family_name,
    aml_address
)


aml_result = client.perform_aml_check(aml_profile)

print("AML Result for {0} {1}:".format(given_names, family_name))
print("On PEP list: " + str(aml_result.on_pep_list))
print("On fraud list: " + str(aml_result.on_fraud_list))
print("On watchlist: " + str(aml_result.on_watch_list))
```

Additionally an [example AML application](/examples/aml/app.py) is provided in the examples folder.

## Running the Examples

From the [Yoti Dashboard](https://www.yoti.com/dashboard/applications):
1. Set the application domain of your app to `localhost:5000`
1. Set the scenario callback URL to `/yoti/auth`

### With Docker

To run the Flask or Django container:
 
1. Clone this repository
1. Change directory to the example project directory with
   * `cd examples/yoti_example_flask` for __Flask__   
   __OR__
   * `cd examples/yoti_example_django` for __Django__
1. Make sure the environment variables `YOTI_SCENARIO_ID`, `YOTI_CLIENT_SDK_ID` and `YOTI_KEY_FILE_PATH` are set (instructions in the [Configuration](#configuration) section). _Please note that with Docker, the .pem file must reside in a location within where docker is being run from, so it should be placed somewhere under the respective  [yoti_example_flask](/examples/yoti_example_flask)/[yoti_example_django](/examples/yoti_example_django) folders._
1. Rebuild the images if you have modified the docker-compose.yml file with
   - `docker-compose build --no-cache`
1. Start the container with `docker-compose up`
1. Navigate to https://localhost:5000

### Running Locally

1. Both example applications utilise the env variables described in [Configuration](#configuration), make sure they are accessible.
1. Ensure pip is up to date: `easy_install --upgrade pip`
1. Ensure setuptools and wheel are up to date: `python -m pip install --upgrade setuptools wheel`

#### Flask

1. Change directories to the Flask project: `cd examples/yoti_example_flask`
1. Install dependencies: `pip install -r requirements.txt`
1. Run `python app.py`
1. Navigate to https://localhost:5000

#### Django

1. You will need Python 3+ to run the Django example
1. Change directories to the Django project: `cd examples/yoti_example_django`
1. Install dependencies: `pip install -r requirements.txt`
1. Apply migrations before the first start by running: `python manage.py migrate`
1. Run: `python manage.py runsslserver 0.0.0.0:5000`
1. Navigate to https://localhost:5000

#### AML Example

1. Change directories to the AML folder: `cd examples/aml`
1. Install requirements with `pip install -r requirements.txt`
1. Run: `python app.py`

## Running the Tests

Running the tests is done by the following process, ensuring you are using Python 3.0+:

1. Install dependencies: `pip install -r requirements.txt`
1. Install the SDK: `python setup.py develop`
1. Execute in the main project dir: `py.test`

## API Coverage

* Activity Details
    * [X] Remember Me ID `user_id`
    * [X] Parent Remember Me ID `parent_remember_me_id`
    * [X] ReceiptID `receipt_id`
    * [X] Timestamp `timestamp`
    * [X] Profile `profile`
        * [X] Photo `selfie`
        * [X] Given Names `given_names`
        * [X] Family Name `family_name`
        * [X] Full Name `full_name`
        * [X] Mobile Number `phone_number`
        * [X] Email Address `email_address`
        * [X] Date of Birth `date_of_birth`
        * [X] Address `postal_address`
        * [X] Gender `gender`
        * [X] Nationality `nationality`
    * [X] Base64 Selfie URI `base64_selfie_uri`

## Support

For any questions or support please email [sdksupport@yoti.com](mailto:sdksupport@yoti.com).
Please provide the following to get you up and working as quickly as possible:

* Computer type
* OS version
* Version of Python being used
* Screenshot

Once we have answered your question we may contact you again to discuss Yoti products and services. If you’d prefer us not to do this, please let us know when you e-mail.

### Windows Configuration
If you're using Windows and you haven't installed Cryptography before, you might need to set two environment variables for Cryptography to install (it is a requirement of the Yoti package):
```shell 
set LIB=C:\OpenSSL-Win64\lib;%LIB%
set INCLUDE=C:\OpenSSL-Win64\include;%INCLUDE%
```
Where `OpenSSL-Win64` is the location that you have installed OpenSSL to. See [here](https://cryptography.io/en/latest/installation/#building-cryptography-on-windows) for more information.
