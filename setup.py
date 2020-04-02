# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

long_description = (
    "This package contains the tools you need to quickly "
    "integrate your Python back-end with Yoti, so that your "
    "users can share their identity details with your "
    "application in a secure and trusted way."
)

version = {}
with open("yoti_python_sdk/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="yoti",
    version=version["__version__"],
    packages=find_packages(include=["yoti_python_sdk", "yoti_python_sdk.*"]),
    license="MIT",
    description="The Yoti Python SDK, providing API support for Login, Verify (2FA) and Age Verification.",
    long_description=long_description,
    url="https://github.com/getyoti/yoti-python-sdk",
    author="Yoti",
    author_email="websdk@yoti.com",
    install_requires=[
        "deprecated==1.2.6",
        "cryptography>=2.2.1",
        "protobuf>=3.1.0",
        "requests>=2.11.1",
        "future>=0.11.0",
        "asn1==2.2.0",
        "pyopenssl>=18.0.0",
        "iso8601==0.1.12",
    ],
    extras_require={
        "examples": [
            "Django>1.11.16",
            "Flask>=0.10",
            "python-dotenv>=0.7.1",
            "django-sslserver>=0.2",
            "Werkzeug==0.15.3",
        ],
        "dev": [
            "pre-commit==1.17.0",
            "pytest>=3.6.0",
            "pytest-cov>=2.7.1",
            "pylint==1.9.4",
            "pylint-exit>=1.1.0",
            "python-coveralls==2.9.3",
            "coverage==4.5.4",
            "mock==2.0.0",
            "virtualenv==20.0.13",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="yoti sdk 2FA multifactor authentication verification identity login register verify 2Factor",
)
