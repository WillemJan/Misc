#!/usr/bin/env python2.7

import pygame_sdl2
pygame_sdl2.import_as_pygame()

from pygame import FULLSCREEN
from pygame.locals import *

from pprint import pprint

import datetime
import os
import sys
import random
import time

import pygame.display
import pygame.draw
import pygame.event
import pygame.font
import pygame.image
import pygame.joystick
import pygame.mouse
import pygame.time

import cell

import requests

TIME_FORMAT = '%H:%M'

def aspect_scale(img, screen_size):
    (bx, by) = screen_size
    ix, iy = img.get_size()

    if ix > iy:
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    scaled_image = pygame.transform.scale(
            img,
            (sx, sy))
    return scaled_image


def load_img(screen_size, cm, img_src='/var/www/static/img/cam.jpg'):
    done = False
    while not done:
        try:
            cm.talk("Loading image")
            img = pygame.image.load(img_src).convert_alpha()
            cm.talk("Scaling image")
            img = aspect_scale(img, screen_size)
            color = img.get_at((1, 1))
            cm.talk("Scaling done")
            return img, color
        except:
            cm.talk("Failed to load image")
            time.sleep(0.5)

def calc_center(screen_size, img_size):
    pos = [0, 0]
    if img_size[0] < screen_size[0]:
        pos[0] = (screen_size[0] - img_size[0]) / 2.0
    if img_size[1] < screen_size[1]:
        pos[1] = (screen_size[1] - img_size[1]) / 2.0
    return tuple(pos)


def fc_color(color):
    fc = [0, 0, 0]
    for i in range(3):
        if color[i] - 128 > 0:
            fc[i] = color[i] - 64 - random.random() * 40
        else:
            if color[i] + 128 < 255:
                fc[i] = color[i] + 64 - random.random() * 40
            else:
                fc[i] = 255
    return tuple(fc)


def render_time(fc, myfont):
    now = str(datetime.datetime.now().strftime(TIME_FORMAT))
    now = myfont.render(now, 1, fc)
    return now


def render_hostname(fc, myfont, hostname):
    rendered_hostname = myfont.render(
            hostname.title(),
            0.7,
            fc)
    return rendered_hostname

'''
                image = image.convert()
                colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)
'''


def event_looper():
    msg = ''
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # mouse move
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            # don't dispatch motion if no button are pressed
            if event.buttons == (0, 0, 0):
                continue
            msg = 'on_mouse_move: x:%i y:%i' % (x, y)

        # mouse action
        elif event.type in (pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP):
            x, y = event.pos
            btn = 'left'
            if event.button == 3:
                btn = 'right'
            elif event.button == 2:
                btn = 'middle'
            elif event.button == 4:
                btn = 'scrolldown'
            elif event.button == 5:
                btn = 'scrollup'
            elif event.button == 6:
                btn = 'scrollright'
            elif event.button == 7:
                btn = 'scrollleft'

            eventname = 'on_mouse_down'

            if event.type == pygame.MOUSEBUTTONUP:
                eventname = 'on_mouse_up'
            msg = "%s: x:%s y:%s btn:%s" % (eventname, x, y, btn)

        # joystick action
        elif event.type == pygame.JOYAXISMOTION:
            msg = 'on_joy_axis: joy:%s axis:%s value:%s' % (
                    event.joy, event.axis, event.value)

        elif event.type == pygame.JOYHATMOTION:
            msg = 'on_joy_hat: event:%s hat:%s value:%s' % (
                    event.joy, event.hat, event.value)

        elif event.type == pygame.JOYBALLMOTION:
            msg = 'on_joy_ball: joy:%s ballid:%s rel0:%i rel1:%i' % (
                    event.joy, event.ballid, event.rel[0], event.rel[1])

        elif event.type == pygame.JOYBUTTONDOWN:
            msg = 'on_joy_button_down: joy:%s btn:%i' % (
                    event.joy, event.button)

        elif event.type == pygame.JOYBUTTONUP:
            msg = 'on_joy_button_up: joy:%s btn:%i' % (
                    event.joy, event.button)

        elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
            if event.type == pygame.KEYUP:
                msg = 'on_key_up: key:%s scancode:%s' % (
                        event.key, event.scancode)

            msg = 'on_key_down: key:%s scandoe:%s unicode:%s' % (
                    event.key, event.scancode, event.unicode)

        elif event.type == pygame.VIDEORESIZE:
            #self._size = event.size
            #self.update_viewport()
            msg = 'VIDEORESIZE %s' %event.size

        return msg


class DisplayNerve:
    initialized = False
    def __init__(self, cm):
        self.cm = cm
        msg = "INIT:Initialization starting"
        self.cm.talk(msg)
        while not self.initialized:
            pygame.init()
            pygame.display.init()
            pygame.font.init()

            modes_avail = pygame.display.list_modes(16)

            if cm.hostname == 'higgsboson':
                self.mode = modes_avail[-1]
            else:
                self.mode = modes_avail[0]

            self.screen = pygame.display.set_mode(
                self.mode,
                NOFRAME | DOUBLEBUF,
                16)

            self.cm.talk("REGISTER:X:%s:Y:%s" % (
                str(self.mode[0]),
                str(self.mode[1])))

            self.initialized = True
            self.cm.talk("INIT:Initialization finished")

        self.load_fonts()
        msg = "FONTS:%s" % [f.title() for f in self.fonts]
        self.cm.talk(msg)

        self.load_images()
        msg = "IMAGES:%s" % [i.title() for i in self.images]
        self.cm.talk(msg)

        quit = False
        nrs = []
        bgs = []

        for i in range(40):
            bgs.append(self.generate_backdrop())
            nrs.append(i)

        i = 0
        JMP = 7
        while not quit:
            if i == 0:
                bg = bgs[random.choice(nrs)]
                bg.set_alpha(0)
                self.screen.blit(bg, (0, 0))
                pygame.display.update()
                i += 1
            elif i < 255:
                if i % JMP == 0:
                    bg.set_alpha(i)
                    self.screen.fill((0,0,0))
                    self.screen.blit(bg, (0, 0))
                    pygame.display.update()
                i += 1
            elif i < 255 * 2:
                if i == 255:
                    bg1 = bgs[random.choice(nrs)]
                    bg1.set_alpha(0)

                if i % JMP == 0:
                    bg1.set_alpha(abs(255-i))
                    bg.set_alpha(255 * 2 - i)
                    pygame.display.update()

                if (i * 2 - 255) / 2 < 127:
                    if i % JMP == 0:
                        self.screen.fill((0,0,0))
                        self.screen.blit(bg1, (0, 0))
                        self.screen.blit(bg, (0, 0))
                        pygame.display.update()
                else:
                    if i % JMP == 0:
                        self.screen.fill((0,0,0))
                        self.screen.blit(bg, (0, 0))
                        self.screen.blit(bg1, (0, 0))
                        pygame.display.update()
                i += 1
            else:
                i = 255
                bg = bg1

                
            event_msg = event_looper()

            if event_msg:
                msg = "EVENT:%s" % event_msg
                self.cm.talk(msg)
            else:
                time.sleep(0.01)
            # msg = cm.listen()
        pygame.quit()

    def load_images(self):
        images = {}

        bpath = __file__.replace(os.path.basename(__file__), '')
        bpath = os.path.join(bpath, 'gfx', 'img')
        image_filenames = os.listdir(bpath)

        for image_filename in image_filenames:
            try:
                path = os.path.join("./", bpath, image_filename)
                name = name = os.path.basename(image_filename).split('.')[0].lower()
                image = pygame.image.load(path).convert()
                colorkey = image.get_at((10, 10))
                image.set_colorkey(colorkey)
                images[name] = image
                msg = "{'load' : True, 'msg' : 'loaded: %s'}" % path
                self.cm.talk(msg)
            except:
                msg = "{'error' : True, 'msg' : 'Failed to load: %s'}" % path
                self.cm.talk(msg)

        self.images = images


    def generate_backdrop(self):
        bg = pygame.Surface((self.mode))
        cart_rect = pygame.Surface((self.mode[0] / 50.0, self.mode[1] / 50.0))
        rnd = random.random()
        rnd1 = random.random()
        for x in range(20):
            for y in range(20):
                color = (20 + x / 2 + x * random.random(),
                         20 + y / 2 + y * random.random(), 0)
                cart_rect.fill((color))
                bg.blit(cart_rect, (x * cart_rect.get_width(),
                                    y * cart_rect.get_height()))
        x = int(rnd1 * 30) + 10
        y = int(rnd * 30) + 10
        im = random.choice(self.images.keys())
        bg.blit(self.images[im], (x * cart_rect.get_width(),
                                 y * cart_rect.get_height()))
        return bg

    def load_fonts(self):
        fonts = {}

        bpath = __file__.replace(os.path.basename(__file__), '')
        bpath = os.path.join(bpath, 'gfx', 'fonts')
        font_filenames = os.listdir(bpath)

        sizes = [15, 18, 23, 25, 27, 28]

        for size in sizes:
            for font_filename in font_filenames:
                if font_filename.endswith('.ttf'):
                    name = os.path.basename(font_filename).split('.')[0].lower()
                    path = "./" + os.path.join(bpath, font_filename)
                    fonts[name] = {}
                    fonts[name][size] = pygame.font.Font(path, size)
        self.fonts = fonts

if __name__ == '__main__':
    cm = cell.Membrane("DISPLAY")
    cm.start()
    DisplayNerve(cm)
    cm.join()
