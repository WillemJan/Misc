#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread

import json
import os
import SocketServer
import time
import zmq

import cell

from pprint import pprint

class Membrane():
    connected = False
    host = "127.0.0.1"
    port = 9990  # Warning: This might flŭkˈcho͞o-ātˌ

    def __init__(self, report_queue, log):
        self.Wand.report_queue = report_queue
        self.log = log

    def setup_listening_membrane(self):
        while not self.connected:
            try:
                server = SocketServer.TCPServer(
                             (self.host, self.port),
                             self.Wand)

                self.server = Thread(target=server.serve_forever)
                self.server.daemon = True
                self.server.start()

                self.connected = ("BOOT:MEMBRANE:tcp://%s:%s" % (
                    self.host,
                    self.port))

                self.log("Listen to Membrane: tcp://%s:%i." % (
                    self.host,
                    self.port))
            except:
                self.log("Failed to setup Membrane: tcp://%s:%i." % (
                    self.host,
                    self.port))
                time.sleep(0.5)
                self.port += 1

    def join(self):
        self.server.join(0.1)

    class Wand(SocketServer.BaseRequestHandler):
        report_queue = None
        nerve_state = {}

        def handle(self):
            data = self.request.recv(1024).strip()
            if data:
                self.report_queue.put(data)
                self.request.sendall(data)


class Nerve():
    host = "10.0.0.254"
    port = "7801"
    temp = False

    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    hostname = cell.hostname()
    socket.identity = hostname
    poll = zmq.Poller()

    instructions = []

    def store_state(self):
        out = os.path.join(
                  cell.www['static'],
                  'nerve_state.json')

        try:
            with open(out, 'wb') as fp:
                json.dump(self.nerve_state, fp)
        except:
            pass

    def log(self, msg):
        print("%s:%s" % (
            str(time.time()),
                msg))

    def establish_connection_to_spine(self):
        self.log("Connecting to Spine: tcp://%s:%s." % (
            self.host,
            self.port))

        self.socket.connect(str("tcp://%s:%s" % (
            self.host,
            self.port)))

        msg = "host:%s msg:event value:{'nervecell' : '%s', 'state' : True}" % (cell.hostname(), cell.hostname())
	self.socket.send_string(msg)

    def heartbeat(self):
        msg = "host:%s msg:event value:{'nervecell' : '%s', 'state' : True}" % cell.hostname()
	self.socket.send_string(msg)

    def __init__(self, host=False, port=False):
        if host:
            self.host = host
        if port:
            self.port = port

        self.establish_connection_to_spine()
        report_queue = Queue(maxsize=0)

        membrane = Membrane(
                report_queue,
                self.log)
        membrane.setup_listening_membrane()
        report_queue.put(membrane.connected)
        if membrane.connected:
            report = membrane.connected
        else:
            report = ''
        membrane_info = {}        
        self.nerve_state = {
             'boot_time': str(time.time()),
             'membrane_host': membrane.host,
             'membrane_port': membrane.port,
             'spine_host': self.host,
             'spine_port': self.port,
             'membrane_info' : membrane_info,
        }
        self.store_state()

        quit = False

        while not quit:
            now = str(time.time())

            if not self.temp:
                temp_count = 0
                temp = os.popen('vcgencmd measure_temp 2> /dev/null').read()
                self.temp = temp
            else:
                temp_count += 1
                temp = self.temp
                if temp_count % 999 == 0:
                    temp = os.popen('vcgencmd measure_temp 2> /dev/null').read()
                    self.temp = temp

            if '=' in temp:
                temp = temp.split('=')[1].strip()
            else:
                temp = 'Unknown'

            msg_body = "host:%s time:%s temp:%s" % (self.hostname, now, temp)
            
            if report:
                if report == 'QUIT':
                    quit = True
                else:
                    msg = u"%s %s" % (
                            msg_body,
                            report)
                print(msg)

                if not 'HEARTBEAT' in msg:
                    self.socket.send_string(msg)
                report = ''
                time.sleep(0.05)

	    #self.heartbeat()
            self.poll.register(self.socket, zmq.POLLIN)
            sockets = dict(self.poll.poll(0.1))

            spine_data = {}
            changed = False

            if self.socket in sockets:
                msg = self.socket.recv()
                if msg:
                    try:
                        new_spine_data = json.loads(msg)
                        if new_spine_data:
                            if not spine_data == new_spine_data:
                                spine_data == new_spine_data
                                changed = True
                    except:
                        pass

                if changed and spine_data:
                    print(spine_data)
            
            while not report_queue.empty():
                report = report_queue.get()
                if report:
                    report = report.strip()
                    #self.log("Membrane input: %s." % report)
                report_queue.task_done()

        for  i in range(10):
            report = 'QUIT'
            msg = u"%s NERVE:%s:%s" % (
                    self.hostname,
                    now,
                    report)
            self.socket.send_string(msg)
            time.sleep(0.0001)

        membrane.join()

if __name__ == '__main__':
    print('nerve start')
    nerve = Nerve()
