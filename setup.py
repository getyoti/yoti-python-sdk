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
        "deprecated==1.2.10",
        "cryptography>=2.2.1",
        "protobuf==3.20.1",
        "requests>=2.11.1",
        "future>=0.11.0",
        "asn1==2.2.0",
        "pyopenssl>=18.0.0",
        "iso8601==0.1.13",
        "pytz==2022.1",
    ],
    extras_require={
        "examples": [
            "Django>=3.0.7",
            "Flask>=1.0.4",
            "python-dotenv>=0.7.1",
            "django-sslserver>=0.22.0",
            "Werkzeug==1.0.1",
        ],
        "dev": [
            "pre-commit==1.17.0",
            "pytest>=4.6.11",
            "pytest-cov>=2.7.1",
            "pylint==1.9.4",
            "pylint-exit>=1.1.0",
            "python-coveralls==2.9.3",
            "coverage==4.5.4",
            "mock==2.0.0",
            "virtualenv==20.1.0",
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
