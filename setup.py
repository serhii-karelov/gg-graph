import sys
from setuptools import setup
from setuptools.command.test import test


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='getgoinggraph',
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
