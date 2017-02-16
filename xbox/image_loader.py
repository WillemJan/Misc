#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
 2013 copy is right, Willem Jan Faber (http://www.fe2.nl) 
'''

import threadding
import pygame
import urllib
import time

images = urllib.urlopen('')


class ImageLoader(threading.Thread):

    """ 
        Single threaded image loader.
    """

    stop = False

    weather_image = {'refresh' : time.time(),
                     'data' : False}
    network_image = {'' : time.time(),
                     'data' : False}

    image_list_white = []
    image_list_green = []
    image_list_yellow = []
    image_list_red = []
    image_list_black = []
    image_list_gray = []


    def run(self):
        while not self.stop:
            if not weather_image:




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

        
if __name__ == "__main__":
    import termios, fcntl, sys, os

    stop = False

    imageloader = ImageLoader()
    imageloader.start()

    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while not stop:
            try:
                c = sys.stdin.read(1)
                imageloder.stop = stop = True
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

