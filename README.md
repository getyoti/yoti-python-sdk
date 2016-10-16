## Executing tests ##

1. Install dependencies: `pip install -r requirements.txt`
1. Install the SDK: `python setup.py develop`
1. Execute in the main project dir: `py.test`

### Testing on multiple Python versions ###

Tests executed using [py.test](http://doc.pytest.org/en/latest/) use your default/virtualenv's Python interpreter.
Testing multiple versions of Python requires them to be installed and accessible on your system.
One tool to do just this is [pyenv](https://github.com/yyuu/pyenv).

1. Install `pyenv`
1. Install Python interpreters you want to test with, e.g. `pyenv install 2.6.9`
1. Execute in the main project dir: `tox`

You can choose a subset of interpreters to test with by running `tox -e <testenv_version>`.
For a list of `<testenv_versions>` see `tox.ini`. Example: `tox -e py26` would run the 
test suite on Python 2.6 (2.6.9 in our case, as installed with `pyenv`).

To install all the Python versions this SDK has been tested against run:

    $ for version in 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 3.6.0b1; do pyenv install $version; done

activate the installed interpreters (run in this directory):

    $ pyenv local 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 3.6.0b1
    
run the tests:

    $ tox

#### Tox Common Issues ####

Supporting multiple Python versions with deps often requiring compilation is not without issues.


For Python versions that do not provide binary wheels for `cryptography`, this
library will have to be compiled (will be done automatically). For this you may
need to install development headers of `openssl`.

On Debian-based systems install them with `apt-get install openssl-dev`

On macOS install them using [homebrew](http://brew.sh/): `brew install openssl`

Install xcode command line tools so we have access to a C compiler and common libs:

    xcode-select --install


See [building cryptography on OS X](https://cryptography.io/en/latest/installation/#building-cryptography-on-os-x)

For Python 2.6 and 2.7 you *might* have to install them via `pyenv` with

    PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs2" pyenv install <python version>

to avoid `cffi` errors related to unicode see: [cffi ucs2 vs ucs4](http://cffi.readthedocs.io/en/latest/installation.html#linux-and-os-x-ucs2-versus-ucs4)

## Examples ##
### Flask ###

Make sure your flask application has access to the following environment variables:
* `YOTI_APPLICATION_ID` - found on the Integrations settings page
* `YOTI_CLIENT_SDK_ID` - found on the Integrations settings page
* `YOTI_VERIFICATION_KEY` - found on the Integrations settings page -> Callback URL -> VERIFY
* `YOTI_KEY_FILE_PATH` - the full path to your security key downloaded from the Keys settings page (e.g. /home/user/.ssh/access-security.pem)

Running: `python examples/yoti_example_flask/app.py`

### Django ###
Dependencies: `pip install -r examples/yoti_example_django/requirements.txt`

Make sure your django application has access to the following environment variables:
* `YOTI_APPLICATION_ID` - found on the Integrations settings page
* `YOTI_CLIENT_SDK_ID` - found on the Integrations settings page
* `YOTI_VERIFICATION_KEY` - found on the Integrations settings page -> Callback URL -> VERIFY
* `YOTI_KEY_FILE_PATH` - the full path to your security key downloaded from the Keys settings page (e.g. /home/user/.ssh/access-security.pem)

You should apply the migrations before the first start by running:<br>
`python examples/yoti_example_django/manage.py migrate`

Running: `python examples/yoti_example_django/manage.py runserver 0.0.0.0:5000`
