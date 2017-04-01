#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

'''
Copyright © 2013 Willem Jan Faber (http://www.fe2.nl) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
* Neither the name of “Fe2“ nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# System lib imports
import os
import random
import urllib

# PyGame imports
from pygame import *
from pygame.locals import *

# Own library imports
from config import *

class Background:
    """
    Load new images from disk, scale them and show
    the weather from time to time.
    """

    # New background image
    new = None

    # Current background image
    current = None

    # Counter to show the wearher in the Netherlands
    counter = 0

    # Interval to show the weather map of the Netherlands
    next_wearher_show = int(random.random()*10) + 5

    def __init__(self):
        # Get a list of images from disk
        self.background_images = os.listdir(BACKGROUND_IMAGES)

        # Load the image from disk and scale it
        self.current = self._load_new()
        self.current = self.current.convert_alpha()
        self.current = self._aspect_scale(self.current,
                (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))


    def _load_new(self):
        # Try to load the new image 
        image_random = random.choice(self.background_images)
        try:
            image_data = image.load(os.path.join(BACKGROUND_IMAGES, image_random))
        except error:
            self.background_images.remove(image_random)
            self._load_new()
        return image_data

    def get_new(self):
        """
        Get new images from disk, 
        and scale them, while keeping the aspect.
        """
        self.counter += 1
        if self.counter == self.next_wearher_show:
            # Set the next interval to show the weather
            next_wearher_show = int(random.random()*10) + 5
            
            # Fether the dutch weather map
            data = urllib.urlopen(KNMI_URL).read()

            # Write weather map to disk
            fh = open('/tmp/weer.png', 'wb')
            fh.write(data)
            fh.close()
            self.new = self._load_new()
        else:
            # Get a random image from disk
            self.new = self._load_new()
        self.new = self.new.convert()
        self.new = self._aspect_scale(self.new,
                (SCREEN_WIDTH, SCREEN_HEIGHT))
        print self.new.get_size()


    def swap(self):
        self.current = self.new

    def _aspect_scale(self, img,(bx,by)):
        """
        Got this routine from:
            http://www.pygame.org/pcr/transform_scale/aspect_scale.py
        """
        ix,iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx/float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by / float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx/float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by
        return transform.scale(img, (sx,sy))
