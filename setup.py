import sys
from setuptools import setup
from setuptools.command.test import test


class PyTest(test):
    def run_tests(self):
        import pytest
        errno = pytest.main([])
        sys.exit(errno)

setup(
    name='gg-graph',
    version='0.0.1',
    author='Serhii Karelov',
    author_email='sergey.karelov@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ],
    packages=['graph'],
    entry_points={
        'console_scripts': [
            'graph=graph.app:main',
        ],
    },
    tests_require=['pytest'],
    test_suite='pytest',
    cmdclass={'test': PyTest},
)
