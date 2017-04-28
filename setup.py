# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '1.2.0'
long_description = 'This package contains the tools you need to quickly ' \
                   'integrate your Python back-end with Yoti, so that your ' \
                   'users can share their identity details with your ' \
                   'application in a secure and trusted way.'

setup(
    name='yoti-python-sdk',
    version=VERSION,
    packages=find_packages(),
    license='OTHER',
    description='Yoti Python SDK for back-end integration.',
    long_description=long_description,
    url='https://github.com/getyoti/python',
    author='Yoti',
    author_email='tech@yoti.com',
    install_requires=['cryptography>=1.4', 'protobuf>=3.0.0',
                      'requests>=2.0.0', 'future>=0.11.0'],
    extras_require={
        'examples': ['Django>=1.9', 'Flask>=0.10'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='',
)
