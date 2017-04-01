#!/usr/bin/env python2.7

#
# Spinal cord, listen's to all signals,
# route's them to where they need to go.
#

from hmac import compare_digest as compare_hash
from pprint import pprint
from collections import OrderedDict

import crypt
import json
import random
import string
import subprocess
import threading
import time
import zmq

import cell

class Spine():
    port = cell.all_cells['higgsboson'].get('port')
    host = cell.all_cells['higgsboson'].get('ip')

    nerves = {}
    nerve_info = {}

    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.identity = cell.hostname()

    lights = cell.lights

    def log(self, msg):
        return

    def aap():
        print("%s: %s" % (
            str(time.time()), msg))

    def light(self, light_name):
	url = self.lights.get(light_name).get('url')
	if self.lights.get(light_name) and self.lights.get(light_name).get('status'):
		url = url % 'on'
		response = cell.req(url, 0.8)
	        if response:
			self.lights[light_name]['status'] = not self.lights[light_name]['status']
	else:
		url = url % 'off'
		response = cell.req(url, 0.8)
		if response:
			self.lights[light_name]['status'] = not self.lights[light_name]['status']


    def __init__(self, host=False, port=False):
        if host:
            self.host = host
        if port:
            self.port = port

        self.log("Booting spinal cord, I will listen and respond to the nerve system.")

        self.log("Binding spine to tcp://%s:%s" % (
            self.host, self.port))

        self.socket.bind(
                str("tcp://%s:%s" % (
                    self.host,self.port)))

        cel_info = {}

        shared_nerve_state = {}

        for count, cel_name in enumerate(
                sorted(cell.all_cells)):

            print("Will listen to: %s (%s)" % (
                cel_name,
                cell.all_cells.get(cel_name).get('ip'),
                ))
            cel_info[cel_name] = {
                    'ip' : cell.all_cells.get(cel_name).get('ip'),
                    'name' : cel_name,
                    'msg_list' : list(),
                    }
        i = 0

        event_list = []
        last = ''

        while True:
            msg = self.socket.recv_multipart()

            if msg:
                msg = ':'.join(msg)

                if not msg.startswith('host:'):
                    print('ERRRORR', msg)
                else:
                    recieved_from = msg.split(':')[1].split(' ')[0]
                    msg = ' '.join(msg.split(' ')[1:])

                    if 'event' in msg.lower():
                        print('recieved_from: %s msg: %s' % (
                            recieved_from, msg))

                        if 'on_key_down: key:1073741886 scandoe:62' in msg or 'on_key_down: key:55 scandoe:36' in msg:
                            print("kitchen")
                            if not last == 'kitchen':
                                self.light("kitchen")
                                last = 'kitchen'
                            else:
                                last = ''

                        if 'on_key_down: key:1073742053 scandoe:229' in msg or 'on_key_down: key:13 scandoe:40' in msg:
                            if not last == 'table':
                                print("table")
                                self.light("table")
                                last = 'table'
                            else:
                                last = ''

                        if 'on_key_down: key:104 scandoe:11' in msg or 'on_key_down: key:51 scandoe:32' in msg:
                            if not last == 'desk2':
                                print("desk2")
                                self.light("desk2")
                                last = 'desk2'
                            else:
                                last = ''

                        if 'on_key_down: key:44 scandoe:54' in msg or 'on_key_down: key:49 scandoe:30' in msg:
                            if not last == 'desk1':
                                print("desk1")
                                self.light("desk1")
                                last = 'desk1'
                            else:
                                last = ''

                        if 'on_key_down: key:47 scandoe:56' in msg or 'on_key_down: key:91 scandoe:47 ' in msg:
                            if not last == 'tv':
                                print("tv")
                                self.light("tv")
                                last = 'tv'
                            else:
                                last = ''

                        if 'leap_controller:EVENT:' in msg:
                            print("**")
                            pprint(json.loads(msg.split('leap_controller:EVENT:')[1]))
                            last_msg = msg
                            print("**")


                '''

            self.socket.send_multipart([cell.hostname(),
                                        json.dumps(shared_nerve_state)])


                if 'HEARTBEAT' in msg:
                    if hostname not in shared_nerve_state:
                        if ':' in msg:
                            #print(msg.split(':')[1])
                            shared_nerve_state[hostname] = {'timing': [1]}
                    else:
                        shared_nerve_state[hostname]['timing'].append(1)
                        sns = shared_nerve_state[hostname]['timing']
                        if len (shared_nerve_state[hostname]['timing']) > 5:
                            sns = sns[1:]
                            shared_nerve_state[hostname]['timing'] = sns
                    sns = shared_nerve_state[hostname]['timing']
                    asns = sum(sns) / float(len(sns))
                    shared_nerve_state[hostname]['avg'] = asns
                #else:
                #    print(msg, '***', hostname)

                if 'EVENT' in msg:
                    if 'leap_controller' in msg and 'fingers' in msg:
                        print(msg.split('fingers')[0].split()[-1])
                        pprint(shared_nerve_state)


                if 'REGISTER' in msg:
                    print(msg)
                    service = msg.split(':')[2]
                    if not hostname in shared_nerve_state:
                        shared_nerve_state[hostname] = {'timing' : []}
                    if 'service' in shared_nerve_state[hostname]:
                        if not service in shared_nerve_state[hostname]['service']:
                            shared_nerve_state[hostname]['service'].append(service)
                    else:
                        shared_nerve_state[hostname]['service'] = [service]


                if 'QUIT' in msg and ':' in msg:
                    rmservice = msg.split(':')[0]
                    print(msg, rmservice)
                    if hostname in shared_nerve_state and 'service' in shared_nerve_state.get(hostname):
                        service = shared_nerve_state[hostname]['service']
                        shared_nerve_state[hostname]['service'] = [s for s in service if not s == rmservice]
                #if 'fingers' in msg:
                #    nr_of_fingers = msg.split(':')[4].split(' ')[2]
            

            if i == 990:
                cls = subprocess.call('clear', shell=True)

                #pprint(shared_nerve_state)
                i = 0
            i += 1
            #time.sleep(0.01)
            topic = 1
            if ':' in string:
                messagedata = ':'.join([j for j in string.split(':')[1:]]).strip()
                if not messagedata in cel_info[topic]['msg_list'] and not 'HEARTBEAT' in messagedata:
                    cel_info[topic]['msg_list'].append(
                            messagedata)
                    if len(cel_info[topic]['msg_list']) > 5:
                        cel_info[topic]['msg_list'].pop(0)
            cel_info[topic]['msg'] = string
            if i % 20 == 0 or i == 0:
                cls = subprocess.call('clear',shell=True)
                for j in sorted(cel_info):
                    pprint(cel_info[j])
                #time.sleep(0.1)
                pass
                '''

if __name__ == '__main__':
    import time
    spine = Spine()
