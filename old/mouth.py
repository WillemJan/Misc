#!/usr/bin/env python

# Mouth system,
# Eats stuff

import hashlib
import os
import sys

from pprint import pprint
from PIL import Image
from StringIO import StringIO


def eat_image(path):
    res = {'format' : '',
           'size_x' : 0,
           'size_y' : 0,
           'md5sum' : ''}

    data = StringIO(open(path, 'rb').read())
    mdsum = hashlib.md5(str(data)).hexdigest()

    try:
        im = Image.open(data)
    except:
        os.unlink(path)
        return

    if im.size[0] < 800 or im.size[1] < 600:
        print("DEL!", path)
        os.unlink(path)

    res['fullpath'] = path
    path = path.replace(os.path.basename(path), '')
    res['path'] = path
    res['md5sum'] = mdsum
    res['size_x'] = int(im.size[0])
    res['size_y'] = int(im.size[1])
    res['format'] = str(im.format).lower().replace('jpeg','jpg')
    fname = "%(size_x)s_%(size_y)s_%(md5sum)s.%(format)s" % (res)
    res['newpath'] = fname
    res['fullnewpath'] = path + fname

    pprint(res)

    of = open('out.sh', 'a+')
    of.write('mv "' + res['fullpath'] + '" "' + res['fullnewpath'] + '"\n')
    of.close()

eat_image(sys.argv[1])
