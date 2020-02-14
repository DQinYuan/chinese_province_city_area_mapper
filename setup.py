# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

from setuptools import setup, find_packages

import addressparser

here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info < (3,):
    sys.exit('Sorry, Python3 is required.')

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('LICENSE', 'r', encoding='utf-8') as f:
    license = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    reqs = f.read()

setup(
    name='addressparser',
    version=addressparser.__version__,
    description='Chinese Address Parser and Extraction Tool,Chinese Province, City and Area Recognition Utilities',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='XuMing',
    author_email='xuming624@qq.com',
    url='https://github.com/shibing624/address-extractor',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='NLP,Simplified Chinese,Chinese geographic information',
    install_requires=reqs.strip().split('\n'),
    packages=find_packages(exclude=['tests']),
    package_dir={'addressparser': 'addressparser'},
    package_data={
        'addressparser': ['*.*', 'LICENSE', '../LICENSE', 'README.*'],
    },
    test_suite='tests',
)
