#!/usr/bin/env python


"""
    Program written by : Willem Jan Faber
    This program is licensed under the LGPLv2 or LGPLv3 license using following text:

      This program is free software; you can redistribute it and/or
      modify it under the terms of the GNU Lesser General Public
      License as published by the Free Software Foundation; either
      version 2 of the License, or (at your option) version 3.
      
      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
      Lesser General Public License for more details.
      
      You should have received a copy of the GNU Lesser General Public
      License along with the program; if not, see <http://www.gnu.org/licenses/>
"""


# needs an x framebuffer.
# Xvfb :25 -screen 0 1024x10000x24 &
#

from subprocess import Popen, PIPE
import os,hashlib

WEBKIT = "/home/aloha/usr/lib/python-webkit2png/webkit2png.py"
#http://www.gnu.org/software/pythonwebkit/
#git clone git://github.com/lkcl/pywebkitgtk.git
target = "http://www.nu.nl/"
hash = hashlib.md5(target.replace('\n','')).hexdigest()
if not os.path.isfile(hash+".jpg"):
    print(target, hash)
    cmd = WEBKIT + " -d :25 -t 180 -F javascript -F plugins -o " + hash + ".jpg" + " " + target
    p = Popen(cmd, shell = True, stdin = PIPE, stdout = PIPE)
    print(p.communicate()[0])
    print(target)
