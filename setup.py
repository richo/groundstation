# -*- coding: utf-8 -*-
#

"""
Package information for groundstation package.
"""

import sys
from setuptools import setup, Command

VERSION = '0.0.0'

requires = [
    ]

class TestCommand(Command):
    """Command for running unittests without install."""

    user_options = [("args=", None, '''The command args string passed to
                                    unittest framework, such as
                                     --args="-v -f"''')]

    def initialize_options(self):
        self.args = ''
        pass

    def finalize_options(self):
        pass

    def run(self):
        import shlex
        import unittest
        test_argv0 = [sys.argv[0] + ' test --args=', 'discover', 'test']
        #For transfering args to unittest, we have to split args
        #by ourself, so that command like:
        #python setup.py test --args="-v -f"
        #can be executed, and the parameter '-v -f' can be
        #transfering to unittest properly.
        test_argv = test_argv0 + shlex.split(self.args)
        unittest.main(module=None, argv=test_argv)

cmdclass = {
        'test': TestCommand,
    }

setup(
        name='groundstation',
        description="A decentralised git syncronisation engine",
        long_description=open('README.md').read(),
        url="https://github.com/richo/groundstation",
        version=VERSION,
        author="Richo Healey",
        author_email="richo@psych0tik.net",
        license="MIT",
        packages=[
            'groundstation',
        ],
        install_requires=requires,
        cmdclass=cmdclass,
    )
