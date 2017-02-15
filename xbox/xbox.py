#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

'''
2013 Willem Jan Faber (http://www.fe2.nl) 
'''

import pygame
from pygame import *
from pygame.locals import *

import os

import array
import math
import cairo
import random
import urllib

from config import *
from background import Background
from menu import RectangleRound

class Xbox:
    move_down = False
    move_up = False

    def __init__(self):
        init()
        font.init()

        mouse.set_visible(0)
        joystick.init()
        joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())][0]
        joysticks.init()
        display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN|DOUBLEBUF, 16)
    

        self.font = font.Font(None, 42)

        self.clock = time.Clock()

        self.screen = display.set_mode(
                        [SCREEN_HEIGHT,
                        SCREEN_HEIGHT])

        self.background = Background()
        self.bg = Surface(self.screen.get_size()) 
        self.screen.fill((0, 0, 0))

    def intro(self):
        pass

    def __get_font_height(self, size, font):
        '''
          Calculate font height
        '''
        data = array.array('c', chr(0) * 1 * 1 * 4)
        img_surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32, 1, 1, 4)
        ctx = cairo.Context(img_surface)
        ctx.select_font_face(font[0], font[1], font[2])
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_font_size(int(size))
        return (((int(ctx.font_extents()[2])), (int(ctx.font_extents()[3]))))


    def text(self,text,size,alpha,font = (("Impact"),cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL) ):
        ''' 
           Render font using the cairo lib
        '''
        (height, width) = self.__get_font_height(size, font)
        width = int((width * len(text) / 2))
        img = pygame.Surface([width,height])
        data = array.array('c',
                    chr(0) * width * height * 4)
        surface = cairo.ImageSurface.create_for_data (data,
                            cairo.FORMAT_ARGB32,
                            width,
                            height,
                            width*4)
        ctx = cairo.Context(surface)
        ctx.select_font_face(font[0],
                            font[1],
                            font[2])
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_font_size(size)
        ctx.set_source_rgba(1, 1, 1, 0.5 + alpha)
        ctx.move_to(0,size - 2)
        ctx.show_text(str(text))
        img = pygame.image.frombuffer(data.tostring(), (width, height), "ARGB")
        return(img)

    def crossfade(self, counter_crossfade, counter_crossfade_max=CROSSFADER_LOOP):
        """
            Simple crossfader loop
        """
        if counter_crossfade == counter_crossfade_max + 1:
            # Get a new background
            self.background.get_new()

        if counter_crossfade > counter_crossfade_max + 255:
            # Set the new backgroud as current
            self.background.swap()
            return 0
        else:
            # 
            counter = (counter_crossfade - counter_crossfade_max) * 2
            self.bg.fill((0, 0, 0))

            # Blit the current background 
            image = self.background.current
            image.set_alpha(200 - counter)
            self._background_blit(image, self.bg)

            # Blit the new background 
            image = self.background.new
            image.set_alpha(counter)
            self._background_blit(image, self.bg)

            self.screen.blit(self.bg, (0,0))
        return counter_crossfade

    def _background_blit(self, src, dest):
        x = (SCREEN_WIDTH - src.get_size()[0]) / 4
        y = (SCREEN_HEIGHT - src.get_size()[1]) / 2
        dest.blit(src, [x, y])

        
    def main(self):
        loop = True

        self.intro()
        counter_crossfade = CROSSFADER_LOOP
        counter_menu = 0
        
        host_txt = self.text('Network status', 30, (abs(math.sin(counter_menu))))
        
        while loop:
            counter_crossfade += 1
            counter_menu += 0.005
            host_txt = self.text('Network status', 30, abs(math.sin(counter_menu)))

            if counter_crossfade > CROSSFADER_LOOP:
                counter_crossfade = self.crossfade(counter_crossfade)

                spacing = 40
                offset = SCREEN_HEIGHT/5
                rect_round = RectangleRound().convert_alpha(self.screen)
                self.screen.blit(rect_round, (0,offset+spacing*0))
                self.screen.blit(host_txt, (0, 115))
        
            events = pygame.event.get()
            self.clock.tick(60)
            mouse.set_pos([800/2,600/2])

            display.update()

            self.move_down = False
            self.move_up = False

            if mouse.get_pos()[1] > 301:
                time.delay(2)
                self.move_down = False
                self.move_up = True
                mouse.set_pos([800/2,600/2])

            if mouse.get_pos()[1] < 299:
                time.delay(2)
                self.move_up = False
                self.move_down = True
                mouse.set_pos([800/2,600/2])

            mouse.set_pos([800/2,600/2])

            if events:
                for event in events:
                    if event.type == JOYBUTTONDOWN:
                        print events

            if self.move_down or self.move_up:
                print self.move_up, self.move_down

            for e in events:
                if e.type == QUIT or \
                        (e.type == KEYDOWN and e.key == K_ESCAPE):
                    loop = False

def run():
    xbox = Xbox()
    xbox.main()
