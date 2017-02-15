#!/usr/bin/python

import os

import random

from PIL import ImageOps
import Image

BASE_PATH = "/home/aloha/code/imagesearch"
HEIGHT = 768
WIDTH = 1024


#
#  This file is part of ImageSearch.
#
#  ImageSearch is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ImageSearch is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ImageSearch. If not, see <http://www.gnu.org/licenses/>.
#


def get_width_height(img_name):
    Image.load(img_name)
    x, y = img.size
    return(x,y)

ve = {}
hz = {}
sq = {}

def assign(target, colorname, img_name):
    if not colorname in target:
        target[colorname] = [img_name]
    else:
        target[colorname].append(img_name)
    return(target)

for dirname in os.walk(BASE_PATH + os.sep + 'output'):
    if len(dirname[-1]) > 1:
        for img_name in dirname[-1]:
            colorname = dirname[-3].split("/")[-1]
            if img_name.find('_ve_') > -1:
                ve = assign(ve, colorname, img_name)
            elif img_name.find('_hz_') > -1:
                hz = assign(hz, colorname, img_name)
            else:
                sq = assign(sq, colorname, img_name)

im_n = Image.new("RGB", (1024, 768), "white")

img_name = random.choice(ve["green_blue"])
im = Image.open(BASE_PATH + os.sep + "output/green_blue/" + img_name)
size = 512, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256, 256))

name = "black_red"
i = random.randrange(0,3)
if i == 0:
    img_name = random.choice(ve[name])
elif i == 1:
    img_name = random.choice(hz[name])
else:
    img_name = random.choice(sq[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (0, 0))

name = "black_green"
i = random.randrange(0,3)
if i == 0:
    img_name = random.choice(ve[name])
elif i == 1:
    img_name = random.choice(hz[name])
else:
    img_name = random.choice(sq[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256, 0))

name = "black_blue"
img_name = random.choice(ve[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256*2, 0))

name = "blue_green"
img_name = random.choice(hz[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256*3, 0))

name = "blue_red"
img_name = random.choice(hz[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (0, 256))

name = "green_red"
img_name = random.choice(hz[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256 * 3, 256))

name = "red_blue"
img_name = random.choice(sq[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (0, 256 * 3))

name = "red_blue"
img_name = random.choice(sq[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (0, 256 * 2))

name = "red_green"
img_name = random.choice(sq[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256, 256 * 2))

name = "white_green"
i = random.randrange(0,3)
if i == 0:
    img_name = random.choice(ve[name])
elif i == 1:
    img_name = random.choice(hz[name])
else:
    img_name = random.choice(sq[name])
im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256 * 2, 256 * 2))

name = "white_red"
i = random.randrange(0,3)
if i == 0:
    img_name = random.choice(ve[name])
elif i == 1:
    img_name = random.choice(hz[name])
else:
    img_name = random.choice(sq[name])

im = Image.open(BASE_PATH + os.sep + "output" + os.sep + name + os.sep + img_name)
size = 256, 256
im = ImageOps.fit(im, size, Image.ANTIALIAS)
im_n.paste(im, (256 * 3, 256 * 2))

im_n.save(BASE_PATH + os.sep + "out.jpg")
