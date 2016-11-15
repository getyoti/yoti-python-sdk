# Yoti Python SDK #

This package integrates your Python back-end with [Yoti](https://www.yoti.com/) allowing you to
securely verify users' identities.

## Example ##

    from yoti import Client

    @app.route('/callback')
    def callback():
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        activity_details = client.get_activity_details(request.args['token'])
        return activity_details.user_profile

For more details and working [Flask](http://flask.pocoo.org/) and [Django](https://www.djangoproject.com/)
applications see [examples/](https://github.com/lampkicking/yoti-sdk-server-python/tree/development/examples).


## The Flow ##

Assuming you created an application and chose `/callback` as your application's callback on [Yoti Dashboard](https://www.yoti.com/dashboard/),
this endpoint will receive a `token` from Yoti API each time user wishes to share information with you (see the example above).
This token, encrypted with the private key from `.PEM` container, will be used to send a request to Yoti
for user's profile details. That's all folks!

For details see [Yoti Developers Docs](https://www.yoti.com/developers/).

## Installation ##

    $ pip install yoti

This SDK works with Python 2.6+ and Python 3.3+ .

## Configuration ##

After creating your application on the [Yoti Dashboard](https://www.yoti.com/dashboard/), you need to download
the `.PEM` key and save it *outside* the repo (keep it private).

The following env variables are then required for the SDK to work:

* `YOTI_CLIENT_SDK_ID` - found on the Integrations settings page
* `YOTI_KEY_FILE_PATH` - the full path to your private key downloaded from the Keys settings page (e.g. /home/user/.ssh/access-security.pem)

The following env variables are additionally used to configure your backend:

* `YOTI_APPLICATION_ID` - found on the Integrations settings page, used to configure the [Yoti Login Button](https://www.yoti.com/developers/#login-button-setup)
* `YOTI_VERIFICATION_KEY` - found on the Integrations settings page -> Callback URL -> VERIFY, used to verify your back-end callback

## Examples ##

Both example applications utilise the env variables described above, make sure they are accessible.
* Installing dependencies: `pip install -e .[examples]`


### Flask ###

* Run `python examples/yoti_example_flask/app.py`

### Django ###

1. Apply migrations before the first start by running:<br>
    `python examples/yoti_example_django/manage.py migrate`
1. Run: `python examples/yoti_example_django/manage.py runserver 0.0.0.0:5000`


### Plugins ###

Plugins for both Django and Flask are in the `plugins/` dir. Their purpose is to make it as easy as possible to use
Yoti SDK with those frameworks. See their respective `README`'s for details.


## Executing tests ##

1. Install dependencies: `pip install -r requirements.txt`
1. Install the SDK: `python setup.py develop`
1. Execute in the main project dir: `py.test`
1. To execute integration tests run: `py.test -c pytest_integration.ini`

### Testing on multiple Python versions ###

Tests executed using [py.test](http://doc.pytest.org/en/latest/) use your default/virtualenv's Python interpreter.
Testing multiple versions of Python requires them to be installed and accessible on your system.
One tool to do just this is [pyenv](https://github.com/yyuu/pyenv)

1. Install `pyenv`
1. Install Python interpreters you want to test with, e.g. `pyenv install 2.6.9`
1. Install project dependencies: `pip install -r requirements.txt`
1. Execute in the main project dir: `tox`
1. In order to execute integration tests run: `tox pytest_integration.ini`

You can choose a subset of interpreters to test with by running `tox -e <testenv_version>`.
For a list of `<testenv_versions>` see `tox.ini`. Example: `tox -e py26` would run the 
test suite on Python 2.6 (2.6.9 in our case, as installed with `pyenv`).

To install all the Python versions this SDK has been tested against run:

    $ for version in 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 3.6.0b3; do pyenv install $version; done

activate the installed interpreters (execute in this directory):

    $ pyenv local 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 3.6.0b3

run the tests:

    $ tox

#### Tox Common Issues ####

Supporting multiple Python versions with dependencies, often requiring compilation, is not without issues.

For Python versions that do not provide binary wheels for `cryptography`, it
will have to be compiled. This will be done automatically, however you may
need to install development headers of `openssl`.

##### On Debian-based systems #####
 
Install `openssl` headers with `apt-get install openssl-dev`

##### On macOS #####
 
Install `openssl` headers using [homebrew](http://brew.sh/): `brew install openssl`

Install xcode command line tools so we have access to a C compiler and common libs:

    xcode-select --install

See [building cryptography on OS X](https://cryptography.io/en/latest/installation/#building-cryptography-on-os-x)


For Python 2.6 and 2.7 you *might* have to install them via `pyenv` with specific unicode code point settings:

    PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs2" pyenv install <python version>

to avoid `cffi` errors related to unicode see: [cffi ucs2 vs ucs4](http://cffi.readthedocs.io/en/latest/installation.html#linux-and-os-x-ucs2-versus-ucs4)
