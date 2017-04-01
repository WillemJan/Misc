#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:author: Willem Jan Faber
:licence: LGPLv2 or LGPLv3.

This program is licensed under the LGPLv2 or LGPLv3 license,
for more info see <http://www.gnu.org/licenses/>.
"""

import getopt
import sys

version = '1.0'
verbose = False
gender = 'f'

try:
    options, remainder = getopt.gnu_getopt(
           sys.argv[1:], 'g:v', ['gender=', 'verbose' ])
except getopt.GetoptError:
    sys.stdout.write('%s -i <inputfile> -o <outputfile>' % sys.argv[0])
    sys.exit(2)


for opt, arg in options:
    if opt in ('-g', '--gender'):
        if arg in ['f','m']:
            gender = arg
        else:
            sys.stdout.write('Unkown gender \'%s\'' % arg)
    elif opt in ('-v', '--verbose'):
        verbose = True

if remainder:
    sys.stdout.write('%s Ignoring %s' % (sys.argv[0] , ",".join(remainder))
