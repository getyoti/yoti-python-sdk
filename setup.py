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
    python_requires=">=3.9",
    install_requires=[


        "asn1==2.2.0",  # still pinned due to enum34 issue
        "cryptography>=42.0.0",
        "protobuf>=4.21.12",
        "requests>=2.31.0",
        "pyopenssl>=24.0.0",
        "pytz>=2025.2",
        "iso8601>=1.1.0",
        "deprecated>=1.2.14",

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
            "coverage>=7.4.0",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",

        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="yoti sdk 2FA multifactor authentication verification identity login register verify 2Factor",
)
