# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        # try:
        #     from multiprocessing import cpu_count
        #     self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        # except (ImportError, NotImplementedError):
        #     self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read_rst(f):
    return open(f, 'r', encoding='utf-8').read()


README = os.path.join(os.path.dirname(__file__), 'README.rst')

requires = [
           'pandas',
           'jieba',
           ]  


setup(name='cpca',
      version='0.4.1',
      description='Chinese Province, City and Area Recognition Utilities',
      long_description=read_rst(README),
      author='DQinYuan',
      author_email='sa517067@mail.ustc.edu.cn',
      url='https://github.com/DQinYuan/chinese_province_city_area_mapper',
      license="MIT",
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
      ],
      keywords='Simplified Chinese,Chinese geographic information,Chinese province city and area recognition and map',
      packages=['cpca', 'cpca.resources'],
      # 通过python setup.py test可以执行所有的单元测试
      cmdclass={'test': PyTest},
      package_dir={'cpca': 'cpca', 'cpca.resources': 'cpca/resources'},
      package_data={'': ['*.csv']},
      include_package_data=True,
      install_requires=requires,
)
