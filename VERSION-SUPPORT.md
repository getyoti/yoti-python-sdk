
# Version Support
Extra information on ensuring correct version of Python is being used
## Testing on multiple Python versions ##

Tests executed using [py.test](http://doc.pytest.org/en/latest/) use your default/virtualenv's Python interpreter.
Testing multiple versions of Python requires them to be installed and accessible on your system.
One tool to do this for Unix systems is [pyenv](https://github.com/yyuu/pyenv)

1. Install `pyenv`
1. Install Python interpreters you want to test with, e.g. `pyenv install 2.6.9`
1. Install project dependencies: `pip install -r requirements.txt`
1. Execute in the main project dir: `tox`

You can choose a subset of interpreters to test with by running `tox -e <testenv_version>`.
For a list of `<testenv_versions>` see `tox.ini`. Example: `tox -e py26` would run the
test suite on Python 2.6 (2.6.9 in our case, as installed with `pyenv`).

To install all the Python versions this SDK has been tested against run:

```shell
$ for version in 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 3.6.3; do pyenv install $version; done
```

Activate the installed interpreters (execute in this directory):

```shell
$ pyenv local 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 3.6.3
```

Run the tests:

```shell
$ tox
```

### Tox Common Issues ###

Supporting multiple Python versions with dependencies, often requiring compilation, is not without issues.

For Python versions that do not provide binary wheels for `cryptography`, it will have to be compiled. This will be done automatically, however, you may need to install development headers of `openssl`.

#### On Debian-based Systems ####

Install `openssl` headers with:
```shell
apt-get install openssl-dev
```

See [Building Cryptography on Linux](https://cryptography.io/en/latest/installation/#building-cryptography-on-linux) for more information. 

#### On Windows #####

- Download and compile the OpenSSL binaries for your architecture from the [OpenSSL release](https://ci.cryptography.io/job/cryptography-support-jobs/job/openssl-release-1.1/) website
- Set the `LIB` and `INCLUDE` environment variables to include your OpenSSL installation location e.g.
```shell
C:\> \path\to\vcvarsall.bat x86_amd64
C:\> set LIB=C:\OpenSSL-win64\lib;%LIB%
C:\> set INCLUDE=C:\OpenSSL-win64\include;%INCLUDE%
C:\> pip install cryptography
```
For more information see the [building for windows](https://cryptography.io/en/latest/installation/#building-cryptography-on-windows) section on the Cryptography website.

#### On macOS ####

Install `openssl` headers using [homebrew](http://brew.sh/): `brew install openssl`

Install Xcode command line tools so we have access to a C compiler and common libs:

```shell
$ xcode-select --install
```

See [building cryptography on OS X](https://cryptography.io/en/latest/installation/#building-cryptography-on-os-x)


For Python 2.6 and 2.7 you *might* have to install them via `pyenv` with specific unicode code point settings:

```
PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs2" pyenv install <python version>
```

To avoid `cffi` errors related to unicode see: [cffi ucs2 vs ucs4](http://cffi.readthedocs.io/en/latest/installation.html#linux-and-os-x-ucs2-versus-ucs4)
