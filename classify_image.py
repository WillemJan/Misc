#!/usr/bin/python


import os

import datetime
import random
import shutil
import threading

# Python imaging
import Image

_author = "WillemJan Faber"

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

def classify(img, img_name):
    max_x, max_y = img.size

    try:
        pix = img.load()
    except:
        return False

    black = white = 0
    red = green = blue = 0
    seen = set()

    x, y = random.randrange(0, max_x - 1), random.randrange(0, max_y - 1)

    # Buffer for seen pixels.
    seen.add((x, y))

    # Start with determining pixel level colors.
    for i in range(max_x / 3 * max_y / 3):
        loop_counter = 0

        while (x, y) in seen and not loop_counter < 10000:
            # Sample a random pixel
            x = random.randrange(0, max_x - 1)
            y = random.randrange(0, max_y - 1)

            # Bail if the loop is infinite
            loop_counter += 1

        # Add the pixels to the buffer,
        # so we don't classify stuff twice.
        seen.add((x, y))

        try:
            r, g, b = pix[random.randrange(0, max_x - 1),
                          random.randrange(0, max_y - 1)]
        except:
            r = g = b = 0

        THRESHOLD = 20

        if r <= THRESHOLD and g <= THRESHOLD and b <= THRESHOLD:
            black += 1
        elif r == g and g == b or (r in range(255 - THRESHOLD, 255) and g in range(255 - THRESHOLD, 255) and b in range(255 - THRESHOLD, 255)):
            white += 1
        elif r >= 255 - THRESHOLD and g >= 255 - THRESHOLD and b >= 255 - THRESHOLD:
            white += 1
        elif  r > g and r > b:
            red += 1
        elif g > b and g > r:
            green += 1
        elif b > r and b > g:
            blue += 1

    # Classify black images
    if black > blue and black > red and black > green and black > white:
        if red > blue and red > green:
            name = "_red"
        elif green > red and green > blue:
            name = "_green"
        elif blue > red and blue > green:
            name = "_blue"
        else:
            name = ""
        return "black" + name
    # Classify white images.
    elif white > blue and white > red and white > green and white > black:
        if red > blue and red > green:
            name = "_red"
        elif green > red and green > blue:
            name = "_green"
        elif blue > red and blue > green:
            name = "_blue"
        else:
            name = ""
        return "white" + name
    # Classify red images.
    elif red > blue and red > green:
        if blue > green:
            return "red_blue"
        else:
            return "red_green"
    # Classify green images.
    elif green > red and green > blue:
        if blue > red:
            return "green_blue"
        else:
            return "green_red"
    # Classify blue images.
    elif blue > red and blue > green:
        if red > green:
            return "blue_red"
        else:
            return "blue_green"
    else:
        # This should not be reach.
        return "black"

    # This is for zombie pixels,
    # and should not be reached.
    return "black"


def run_classifier(img_fullname, img_basename):
    try:
        img_data = Image.open(img_fullname)
        max_x, max_y = img_data.size
        if max_x < 250 or max_y < 250:
            cl = False
        else:
            cl = True
    except:
        cl = False

    if cl:
        result = classify(img_data, img_fullname)
        print(result, img_fullname)
        if result:
            now = str(datetime.datetime.now()).replace(' ', '_').split('.')[1]
            if not os.path.isdir("output" + os.sep + result):
                try:
                    os.mkdir("output" + os.sep + result)
                except:
                    # Threadsafe ;)
                    pass

            if max_y == max_x or max_y in range(max_x - 20, max_x + 20):
                shutil.copyfile(img_fullname,
                        "./output/" + result + os.sep + now + "_" + "sq" + "_" + img_basename)
            elif max_y > max_x:
                shutil.copyfile(img_fullname,
                        "./output/" + result + os.sep + now + "_" + "hz" + "_" + img_basename)
            else:
                shutil.copyfile(img_fullname,
                        "./output/" + result + os.sep + now + "_" + "ve" + "_" + img_basename)


def classify_dir(dirname):
    threads = []

    if len(dirname[-1]) > 1:
        for img_basename in dirname[-1]:
            img_fullname = dirname[0] + os.sep + img_basename
            run_classifier(img_fullname, img_basename)

threads = []

'''
dirs = ['/home/aloha/nobackup/archive_org/',
        '/home/aloha/www/WillemJan_Faber/mirror.fe2.nl/www.wga.hu/art/',
        '/home/aloha/www/WillemJan_Faber/mirror.fe2.nl/www.ibiblio.org/',
        '/home/aloha/nobackup/image_of_the_day/',
        '/home/aloha/cache/twitter/']
'''

dirs = ['/home/aloha/nobackup/image_of_the_day/']

for topdirname in dirs:
    for dirname in os.walk(topdirname):
        classify_dir(dirname)
