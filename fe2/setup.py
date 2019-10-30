#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'test':
    os.system('python test_requests.py')
    sys.exit()

entry_point = ("""
        [console_scripts]
        noise=Fe2.tools.alsa:noise
        mute=Fe2.tools.alsa:mute
""")

required = ['requests==2.20.0',
            'pymongo',
            'pymetar',
            'pyalsaaudio',
            'sqlalchemy',
            'pysqlite',
            'flask',
            'speedparser',
            'ipcalc',
            'Sphinx',
            'nltk',
            'python-Levenshtein',
            'PyFlakes',
            'bicop']
setup(
    name='Fe2',
    version=1,
    description='Fe2Libz',
    email='willemjan@fe2.nl',
    author='Willem Jan Faber',
    url='http://python-requests.org',
    scripts=['src/Fe2/bin/news'],
    package_dir={'': 'src'},
    packages=['Fe2', 'Fe2.tools'],
    install_requires=required,
    license='PIZZA',
    entry_points=entry_point,
)
