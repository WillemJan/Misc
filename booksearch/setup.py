#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for BookSearch"""

import os
import sys

try:
    from setuptools import setup
    print("Rolling with 'setuptools'")
except ImportError:
    from distutils.core import setup
    print("Rolling with 'distutils.core'")

if sys.argv[-1] == 'test':
    os.system('python run-tests.py')
    sys.exit()

# define entry points
entry_point = ("""
    [console_scripts]
    bs=scripts.bs:main
""")

required = ['isbnlib',
            'pycountry',
            'pymarc',
            'lxml',
            'PyZ3950',
            'six>=1.2.0',
            'ply', # req. by z39.50
            'requests']

setup(  # Setup BookSearch scipts and modules.
    name='BookSearch',
    version='0.1',
    description='Willem Jan Faber''s python scripts',
    author_email='willemjan@fe2.nl',
    author='Willem Jan Faber',
    url='http://www.fe2.nl',
    #scripts=['bs'],
    package_dir={'booksearch': 'booksearch'},
    zip_safe=False,
    long_description=__doc__,
    packages = ['booksearch',
                'booksearch.endpoints', 
                'booksearch.formats', 
                'booksearch.protocols', 
                'scripts'],
    install_requires=required,
    license='BSD',
    entry_points=entry_point)
