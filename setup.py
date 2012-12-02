#!/usr/bin/python

from distutils.core import setup

setup(name='tout',
        version='0.1',
        description='Python client and wrapper for the Tout API',
        author='Jeremia Kimelman',
        author_email='jeremia@tout.com',
        url='http://developer.tout.com',
        #package_dir = {'': 'client'},
        packages = ['tout'],
        install_requires=['requests', 'simplejson'],
        license='MIT',
        )
