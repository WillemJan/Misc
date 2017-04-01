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
            cm.talk("DISPLAY:Loading image")
            img = pygame.image.load(img_src).convert_alpha()
            cm.talk("DISPLAY:Scaling image")
            img = aspect_scale(img, screen_size)
            color = img.get_at((1, 1))
            cm.talk("DISPLAY:Scaling done")
            return img, color
        except:
            cm.talk("DISPLAY:Failed to load image")
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


def load_fonts():
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
    return fonts


def load_images():
    images = {}

    bpath = __file__.replace(os.path.basename(__file__), '')
    bpath = os.path.join(bpath, 'gfx', 'img')
    image_filenames = os.listdir(bpath)

    for image_filename in image_filenames:
        path = os.path.join("./", bpath, image_filename)
        name = name = os.path.basename(image_filename).split('.')[0].lower()
        image = pygame.image.load(path).convert()
        colorkey = image.get_at((10, 10))
        image.set_colorkey(colorkey)
        images[name] = image
    return images

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


def main(cm):
    msg = "DISPLAY:INIT:Initialization starting"
    cm.talk(msg)
    initialized = False

    while not initialized:
        pygame.init()
        pygame.display.init()
        pygame.font.init()

        modes_avail = pygame.display.list_modes(16)

        if cm.hostname == 'higgsboson':
            mode = modes_avail[-1]
        else:
            mode = modes_avail[0]

        screen = pygame.display.set_mode(
            mode,
            NOFRAME | DOUBLEBUF,
            16)

        for i in range(10):
            cm.talk("DISPLAY:REGISTER:X:%s:Y:%s" % (
                str(mode[0]),
                str(mode[1])))
            time.sleep(0.001)

        initialized = True
        cm.talk("DISPLAY:INIT:Initialization finished")

    fonts = load_fonts()
    msg = "DISPLAY:FONTS:%s" % [f.title() for f in fonts]
    cm.talk(msg)

    images = load_images()
    msg = "DISPLAY:IMAGES:%s" % [i.title() for i in images]
    cm.talk(msg)

    quit = False

    bs = range(100, 255, 8)

    PADDING = int(mode[1] / 100.0)

    i = 0

    brightness = 0.01


    bgs = []
    cart_rect = pygame.Surface((mode[0] / 50.0, mode[0] / 50.0))

    for i in range(10):
        bg = pygame.Surface((mode))
        bg.fill((0, 0, 0))
        for x in range(40):
                for y in range(40):
                    rnd = random.random()
                    rnd1 = random.random()
                    c = 160 - (y * 4  * (random.random()))
                    if rnd < 0.3:
                        r = 1 - (1 / ((rnd1 + 1 / c) * 2))
                        g = 1 - (1 / ((rnd1 + 1 / c) * 4))
                        b = 1 / c
                    elif rnd < 0.6:
                        r = 1 - (1 / ((rnd / 3 + 1 / c) * 2))
                        g = 1 - (1 / ((rnd1 + 1 / c) * 4))
                        b = 1 / c
                    else:
                        r = 1 - (1 / ((rnd / 3 + 1 / c) * 2))
                        g = 1 - (1 / ((rnd1 / 2 + 1 / c) * 4))
                        b = 1 / c

                    r = abs(r)
                    g = abs(g)
                    b = abs(b)

                    if r > 1:
                        r = 1
                    if g > 1:
                        g = 1
                    if b > 1:
                        b = 1

                    color = (r * c, g * c, b * c)

                    cart_rect.fill((color))

                    bg.blit(cart_rect, (x * cart_rect.get_width(),
                                        y * cart_rect.get_height()))

        bgs.append(bg)
         

    screen.fill((0, 0, 0))

    refresh_logo = True

    while not quit:
        stime = time.time()

        xpos = (mode[0] -
                PADDING - (brightness * PADDING * 200))

        rnd = random.random()

        if refresh_logo:
            ypos = mode[1] - images['logo'].get_height() - cart_rect.get_height() * (rnd * 10)
            for i in bs:
                if rnd < 0.3:
                    color = (i, rnd1, 0)
                elif rnd < 0.6:
                    color = (i, rnd1, 0)
                else:
                    color = (i, i, i)

                if i % 7 == 0:
                    screen.blit(bgs[int(random.random() * len(bgs))], (0,0))

                alpha = i * brightness
                images['logo'].set_alpha(alpha)

                screen.blit(images['logo'],
                        (xpos, ypos + PADDING))
                pygame.display.update()

                time.sleep(0.01)

            for i in bs:
                i = 255 - i
                if rnd < 0.3:
                    color = (i, rnd1, 0)
                elif rnd < 0.6:
                    color = (i, rnd1, 0)
                else:
                    color = (i, i, i)

                if i % 7 == 0:
                    screen.blit(bgs[int(random.random() * len(bgs))], (0,0))

                alpha = i * brightness
                images['logo'].set_alpha(alpha)

                screen.blit(images['logo'],
                        (xpos, ypos + PADDING))

                pygame.display.update()
                time.sleep(0.01)

        else:
            if i % 99 == 0:
                images['logo'].set_alpha(255)
                xpos = (mode[0] -
                        PADDING - (brightness * PADDING * 200))
                screen.blit(bgs[int(random.random() * len(bgs))], (0,0))

                rnd = random.random()

                #screen.blit(bgs[int(random.random() * len(bgs))], (0,0))
                screen.blit(images['logo'], (xpos, ypos + PADDING))
                pygame.display.update()
                #msg = "DISPLAY:LOOP:%s" % str(time.time()-stime)
                #cm.talk(msg)
            i += 0.1

        if brightness < 0.9:
            brightness += 0.09
        else:
            refresh_logo = False
            pass

        #if int(time.time()) % 9 == 0:

        event_msg = event_looper()

        if event_msg:
            msg = "DISPLAY:EVENT:%s" % event_msg
            cm.talk(msg)


    pygame.quit()

if __name__ == '__main__':
    cm = cell.Membrane()
    cm.start()
    main(cm)
