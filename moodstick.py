#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
 Willem Jan Faber
'''


import os
import pygame
import time
import usb
import mpd

from fe2.moodsticks.leds import LED_controll

class MoodMusic():
    current_playlist = None

    def __init__(self, host="192.168.0.1", port="5000"):
        self.host = host
        self.port = port
        self.reconnect()

    def reconnect(self):
        try:
            self.client = mpd.MPDClient()
            self.client.connect(self.host, self.port)
        except:
            self.client = None

    def get_current_mood(self):
	print self.client
        if not self.client:
            self.reconnect()
            return ['gray']

        if not self.current_playlist:
            try:
                self.current_playlist = [f['file']  for f in self.client.playlistinfo()]
            except:
                self.reconnect()
                return
        time.sleep(0.05)
        try:
            current_file = self.client.currentsong().get('file')
        except:
            self.reconnect()
            return

        if current_file and not current_file in self.current_playlist:
            try:
                self.current_playlist = [f['file']  for f in self.client.playlistinfo()]
            except:
                self.reconnect()
                return
        self.playlists = {}
        for color in [i["playlist"] for i in  self.client.listplaylists()]:
            if not color in self.playlists:
                songs = self.client.listplaylist(color)
                self.playlists[color] = songs
            else:
                songs = self.playlists[color]
            if sorted(self.current_playlist) == sorted(songs):
                return([color])
        return(['gray'])


    def change_mood(self, new_mood):
        j = 100
        for i in range(0, 30):
            j -= 2
            time.sleep(0.1)
            try:
                self.client.setvol(int(j))
            except mpd.ConnectionError:
                self.reconnect()
                self.change_mood(new_mood)

        if not self.client:
            self.reconnect()
            return
        try:
            self.client.clear()
            self.client.load(new_mood)
            self.client.play()
        except mpd.ConnectionError:
            self.reconnect()
            self.change_mood(new_mood)

        for i in range(0, 30):
            j += 2
            time.sleep(0.1)
            try:
                self.client.setvol(int(j))
            except mpd.ConnectionError:
                self.reconnect()
                self.change_mood(new_mood)


class MoodSticks():
    seen = []
    moodsticks = {  "black"  : False,
                    "red" 	 : False,
                    "yellow" : False,
                    "green"	 : False,
                    "white"  : False}

    def __init__(self, monitor, music):
        self.screen = monitor.screen
        self.music = music
        for color in self.moodsticks:
            devid_path = os.path.join(color, ".devnum")
            if os.path.isfile(devid_path):
                with open(devid_path, "r") as fh:
                    self.moodsticks[color] = fh.read().strip()

        #if not any(self.moodsticks.values()):
        #    self.initial_setup()

    def scan(self):
        current = []
        busses = usb.busses()
        for bus in busses:
            devices = bus.devices
            for dev in devices:
                for color, devid in self.moodsticks.iteritems():
                    if str(dev.idVendor + dev.idProduct) == devid:
                        current.append(color)
        if current:
            return current
        return self.music.get_current_mood()

    def initial_setup(self):
        #self.stdscr.addstr(0, 0, "Moodtick recorder..")
        #self.stdscr.addstr(2, 0, "Please remove all 'moodsticks', and hit any key..")
        #c = self.stdscr.getch()
        #self.stdscr.clear()
        #self.stdscr.refresh()

        busses = usb.busses()
        for bus in busses:
        	devices = bus.devices
            	for dev in devices:
            		self.seen.append(dev.idVendor + dev.idProduct)

        for color in self.moodsticks:
            devid = self._record(color)
            self.moodsticks[color] = devid
            self.seen.append(devid)
            if not os.path.isdir(color):
                os.mkdir(color)
            devid_path = os.path.join(color, ".devnum")
            with open(devid_path, 'w') as fh:
                fh.write(str(devid))

    def _record(self, color):
        self.stdscr.addstr(0, 0, "Moodtick recorder..")
        self.stdscr.addstr(2, 0, "Please insert the '%s-moodstick'." % color)
        self.stdscr.refresh()
        while True:
            time.sleep(0.2)
            busses = usb.busses()
            for bus in busses:
                devices = bus.devices
                for dev in devices:
                    if not dev.idVendor + dev.idProduct in self.seen:
                        return dev.idVendor + dev.idProduct

class MoodScreen():
    font = None
    screen = None
    fps = 20

    def __init__(self):
        self.screen = pygame.display.set_mode()
        pygame.mouse.set_visible(False)
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        self.font_large = pygame.font.SysFont("freesans", 50)
        self.font_small = pygame.font.SysFont("freesans", 20)
        pygame.display.update()
        self.clock = pygame.time.Clock()

        for i in range(255/2):
            if i% 4 == 0:
                self.screen.fill((i, i, i))
                pygame.display.flip()

        self.text = self.font_large.render('RasMood', True, (0,0,0))
        self.screen.blit(self.text, (100, 100))
        pygame.display.flip()


    def display_mood(self, mood):
        i = 255/2
        self.screen.fill((i, i, i))
        self.text = self.font_large.render('RasMood %s' % mood, True, (pygame.Color(mood)))
        self.screen.blit(self.text, (100, 100))
        pygame.display.flip()


music = MoodMusic()
screen = MoodScreen()
ms = MoodSticks(screen, music)
current_mood = ms.scan()
leds = LED_controll()
if current_mood[0] == 'gray':
    current_mood = music.get_current_mood()
screen.display_mood(current_mood[0])

while True:
    sticks_mood = ms.scan()
    mpd_mood = music.get_current_mood()
    time.sleep(0.5)
    prev_stick_handled = False
    if not sticks_mood == current_mood == mpd_mood:
        print(mpd_mood, current_mood)
        if not mpd_mood == current_mood:
            current_mood = mpd_mood
            screen.display_mood(current_mood[0])
            for i in range(0,80):
                leds.painting_max(rnd=True, s=0.01)
                leds.spaceship_max(rnd=True, s=0.01)
            time.sleep(2.2)
        else:
            current_mood = sticks_mood
            screen.display_mood(current_mood[0])
            for i in range(0,80):
                leds.painting_max(rnd=True, s=0.01)
                leds.spaceship_max(rnd=True, s=0.01)
            music.change_mood(current_mood[0])
            time.sleep(2.2)
