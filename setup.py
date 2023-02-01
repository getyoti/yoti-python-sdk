# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = {}
with open("yoti_python_sdk/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="yoti",
    version=version["__version__"],
    packages=find_packages(include=["yoti_python_sdk", "yoti_python_sdk.*"]),
    license="MIT",
    description="The Yoti Python SDK, providing API support for Login, Verify (2FA) and Age Verification.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/getyoti/yoti-python-sdk",
    author="Yoti",
    author_email="websdk@yoti.com",
    install_requires=[
        "deprecated==1.2.13",
        "cryptography>=2.2.1",
        "protobuf==3.13.0",
        "requests>=2.11.1",
        "future>=0.18.2",
        "asn1==2.2.0",
        "pyopenssl>=18.0.0",
        "iso8601==1.0.2",
        "wheel==0.37.1",
        "pytz==2022.7.1",
    ],
    extras_require={
        "examples": [
            "Django>=3.0.7",
            "Flask>=1.0.4",
            "python-dotenv>=0.7.1",
            "django-sslserver>=0.22.0",
            "Werkzeug==2.1.2",
        ],
        "dev": [
            "pre-commit==2.16.0",
            "pytest>=4.6.11",
            "pytest-cov>=2.7.1",
            "pylint==1.9.4",
            "pylint-exit>=1.1.0",
            "python-coveralls==2.9.3",
            "coverage==4.5.4",
            "mock==2.0.0",
            "virtualenv==20.15.1",
            "flake8==4.0.1",
            "pip-tools==6.6.2",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="yoti sdk 2FA multifactor authentication verification identity login register verify 2Factor",
)
