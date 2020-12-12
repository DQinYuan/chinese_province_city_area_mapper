# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from setuptools import setup
from setuptools.command.test import test as TestCommand

import cpca


class PyTest(TestCommand):

    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = []
        # try:
        #     from multiprocessing import cpu_count
        #     self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        # except (ImportError, NotImplementedError):
        #     self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


README = Path(__file__).parent / 'README.rst'

requires = [
           'pandas',
           'pyahocorasick'
           ]


setup(
    name='cpca',
    version=cpca.__version__,
    description='Chinese Province, City and Area Recognition Utilities',
    long_description=README.read_text(),
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
    keywords=(
        'Simplified Chinese,'
        'Chinese geographic information,'
        'Chinese province city and area recognition and map'),
    packages=['cpca', 'cpca.resources'],
    # 通过python setup.py test可以执行所有的单元测试
    cmdclass={'test': PyTest},
    package_dir={'cpca': 'cpca', 'cpca.resources': 'cpca/resources'},
    package_data={'': ['*.csv']},
    include_package_data=True,
    install_requires=requires,
)
