#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: Fe2.tools.
"""

import os
import sys
import pickle


"""
:author: Willem Jan Faber
:licence: LGPLv2 or LGPLv3.

This program is licensed under the LGPLv2 or LGPLv3 license,
for more info see <http://www.gnu.org/licenses/>.
"""


def main(arg):
    for i in range(10):
        if os.path.isfile(i+str(
        p = pickle.load(fh)

if __name__ == "__main__":
    main(sys.argv)

