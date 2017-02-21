#!/usr/bin/env python

import pygame
import requests
import time

pygame.init()
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
clock = pygame.time.Clock()


print 'state!'
state = { 0 : {
                'url' : 'http://light1/painting/?mode=%s',
                'state' : False
            },
            1 : {
                'url' : 'http://127.0.0.1/light/?nr=16&%s=1',
                'state' : False
            },
            2 : {
                'url' : 'http://127.0.0.1/light/?nr=11&%s=1',
                'state' : False
            },
            3 : {
                'url' : 'http://127.0.0.1/light/?nr=15&%s=1',
                'state' : False
            },
            6 : {
                'url' : 'http://127.0.0.1/light/?nr=4&%s=1',
                'state' : False
            },
            7 : {
                'url' : 'http://127.0.0.1/light/?nr=1&%s=1',
                'state' : False
            }
        }


while 1:
    for event in pygame.event.get():
        print 'axis0', my_joystick.get_axis(0),  'axis1', my_joystick.get_axis(1) 
        #print(event)
        for i in range(0, my_joystick.get_numbuttons()):
            if my_joystick.get_button(i): 
                if i in state:
                    print(i, my_joystick.get_button(i))
                    url = state.get(i).get('url')
                    if state[i]['state']:
                        url = url % "on"
                    else:
                        url = url % "off"
                    state[i]['state'] = not state[i]['state']

                    try:
                        requests.get(url, timeout=0.2)
                    except:
                        pass
                    pygame.event.clear()
                    break
                break
                pygame.event.clear()
    clock.tick(60)
pygame.quit()
