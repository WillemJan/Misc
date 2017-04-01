#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Setup script for Fe2 """

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#TODO: implement test.
if sys.argv[-1] == 'test':
    os.system('python test_requests.py')
    sys.exit()

# define entry points
entry_point = ("""
        [console_scripts]
        ioth=scripts.ioth:ioth
""")

required = ['bicop',
            'book.isbn',
            'configobj',
            'distribute',
            'feedparser',
            'flask',
            'guess_language',
            'httplib2',
            'ipcalc',
            'lxml',
            'nltk',
            'pil',
            'pyalsaaudio',
            'PyFlakes',
            'pyinotify',
            'pymetar',
            'pymongo',
            'python-Levenshtein',
            'requests', 
            'Sphinx',
            'sqlalchemy',
            'sqlitedict',
            'twisted'
            ]

setup(  # Setup Fe2 scipts and modules.
    name='fe2',
    version=1,
    description='Willem Jan Faber''s python scripts',
    email='willemjan@fe2.nl',
    author='Willem Jan Faber',
    url='http://python-requests.org',
    scripts=['src/scripts/ioth.py'],
    package_dir={'': 'src'},
    packages=['fe2', 'fe2.helpers', 'scripts'],
    install_requires=required,
    license='BSD',
    entry_points=entry_point,
)
