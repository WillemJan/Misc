#!/usr/bin/env python2.7

import os
import pigpio
import pygame
import requests
import time

import cell

prev_pos = {
    'x': 0.0,
    'y': 0.0,
}

state = {
    0: {
        'state': False,
        'name': 'Woman',
        'nr': 24,
    },
    1: {
        'state': False,
        'name': 'Table',
        'nr': 15,
    },
    2: {
        'state': False,
        'name': 'Kitchen',
        'nr' : 7,
    },
    3: {
        'state': False,
        'name': 'Desk celing',
        'nr': 14,
    },
    6: {
        'state': False,
        'name': 'Desk left',
        'nr': 23,
    },
    7: {
        'state': False,
        'name': 'Desk right',
        'nr': 18,
    },
}

# 14
# Desk left!
# >>> pi.write(23, 0)

if __name__ == "__main__":
    name = os.path.basename(__file__)
    name = name.replace('_nerve.py', '')
    cm = cell.Membrane(name)
    cm.start()
    cm.talk("BOOT")

    initialized = False
    while not initialized:
        pygame.init()
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            name = joystick.get_name()
            cm.talk("%s:%s" % (
                'REGISTER',
                name))
            initialized = True
        except:
            msg = 'Failed to initialize joystick.'
            cm.talk("%s:%s" % (
                'INIT',
                msg))
            time.sleep(1)

    quit = False

    while not quit:
        print('pump')
        pygame.event.pump()
        msg = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                msg = 'QUIT'
            elif event.type == pygame.JOYHATMOTION:
                msg = ('on_joy_hat', event.joy, event.hat, event.value)
            elif event.type == pygame.JOYBALLMOTION:
                msg = ('on_joy_ball', event.joy,
                        event.ballid, event.rel[0], event.rel[1])
            elif event.type == pygame.JOYBUTTONDOWN:
                msg = ('on_joy_button_down', event.joy, event.button)
            elif event.type == pygame.JOYBUTTONUP:
                msg = ('on_joy_button_up', event.joy, event.button)

        if msg:
            cm.talk("SIGNAL:%s" % str(msg))

        x = int(round(
            joystick.get_axis(0) * 1000))
        y = int(round(
            joystick.get_axis(1) * 1000))

        if not abs(prev_pos['x'] - x) < 20:
            prev_pos['x'] = x
            cm.talk("%s:%s" % ("X", x))

        if not abs(prev_pos['y'] - y) < 20:
            prev_pos['y'] = y
            cm.talk("%s:%s" % ("Y", y))

        for button in [btn for btn in range(0, joystick.get_numbuttons())
                       if joystick.get_button(btn)]:

            cm.talk("%s:%s" % (
                "BUTTON",
                str(button)))

            if button in state:
                cm.talk("%s:%s" % (
                    "EVENT",
                    state[button]['name']))

                nr = state[button]['nr']

                pi = pigpio.pi()
                if state[button]['state']:
                    pi.set_mode(nr, pigpio.OUTPUT)
                    pi.write(nr, 0)
                else: 
                    pi.set_mode(nr, pigpio.OUTPUT)
                    pi.write(nr, 1)
                state[button]['state'] = not state[button]['state']
            else:
                print('Undefined button pressed: %i' % button)
        time.sleep(0.01)

    cm.join()
    pygame.quit()
