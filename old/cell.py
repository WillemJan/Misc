#!/usr/bin/env python

import time
import json
import os
import socket
from threading import Thread

import Queue

req = False

try:
    import requests
    requests_avail = True
except:
    import urllib
    requests_avail = False

__all__ = [
        'all_cells',
        'Membrane',
        'hostname',
        'www']

all_cells = {
    'bpi1': {
        'ip': '10.0.0.71',
        'name': 'bpi1',
        },
    'cam0': {
        'ip': '10.0.0.21',
        'name': 'cam0',
        },
    'display0': {
        'ip': '10.0.0.40',
        'name': 'display0',
        },
    'light0': {
        'ip': '10.0.0.10',
        'name': 'light0',
        },
    'light1': {
        'ip': '10.0.0.11',
        'name': 'light1',
        },
    'touch0': {
        'ip': '10.0.0.30',
        'name': 'touch0',
        },
    'higgsboson' : {
        'ip': '10.0.0.254',
        'name': 'higgsboson',
        'port': '7801',
    }
}


lights = {
    'desk1' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=15&%s', },
    'desk2' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=4&%s', },
    'table' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=16&%s', },
    'tv' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=1&%s', },
    'painting1' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=5&%s', },
    'painting2' : {
            'status' : False,
            'url'    : 'http://light1/painting/?mode=%s', },
    'storage' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=11&%s', },
    'kitchen' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=11&%s', },
    'hallway' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=10&%s', },
    'bathroom' : {
            'status' : False,
            'url'    : 'http://light0/light/?nr=6&%s', },
    'hallway1' : {
            'status' : False,
            'url'    : 'http://display0/light/?nr=8&%s', },
    'hallway2' : {
            'status' : False,
            'url'    : 'http://display0/light/?nr=9&%s', },
    'shelf1' : {
            'status' : False,
            'url'    : 'http://display0/light/?nr=15&%s', },
    'shelf2' : {
            'status' : False,
            'url'    : 'http://display0/light/?nr=16&%s', },
    'magic orb off' : {
            'status' : False,
            'url'    : 'http://bpi1/light/?mode=off&%s', },
    'magic orb red' : {
            'status' : False,
            'url'    : 'http://bpi1/light/?mode=red&%s', },
    'magic orb green' : {
            'status' : False,
            'url'    : 'http://bpi1/light/?mode=green&%s', },
    'magic orb blue' : {
            'status' : False,
            'url'    : 'http://bpi1/light/?mode=blue&%s', },
    'magic orb cyan' : {
            'status' : False,
            'url'    : 'http://bpi1/light/?mode=cyan&%s', },
}


all_membrane_capabilities = [
        'display',
        'xbox_controller',
        'leap',
        'camera',
]

www = {
    'static': '/var/www/static/',
}

def req(url, timeout=0.2):
    ''' Get URL, only return False or True depending on success. '''
    if url:
        if requests_avail:
            try:
                resp = requests.get(url, timeout=timeout)
                return resp.ok
            except:
                return False
            return False
        else:
            try:
                resp = urllib.urlopen(url).read()
                if resp:
                    return True
                return False
            except:
                return False

def hostname():
    ''' Return hostname of system. '''
    hostname = str(socket.gethostbyaddr(
            socket.gethostname())[0]).split('.')[0]
    return hostname

class Receptor(Thread):
    quit = False
    daemon = True
    q = Queue.Queue()

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        import time
        while not self.quit:
            time.sleep(0.1)
            pass

class Membrane(Thread):
    port = '9990'
    host = '127.0.0.1'

    hostname = ''

    nerve_state = {}
    retry_max = 10

    quit = False
    daemon = True
    q = Queue.Queue()

    name = "UNKNOWN"

    def __init__(self, name=False):
        Thread.__init__(self)
        if name:
            self.name = name

    def run(self):
        self._talk()

    def read_nerve_state(self):
        nerve_state_file = os.path.join(
                www['static'],
                'nerve_state.json')

        if os.path.isfile(nerve_state_file):
            nerve_state_modified = os.path.getmtime(nerve_state_file)
            if not ('modified' in self.nerve_state or nerve_state_modified == self.nerve_state.get('modified')):
                with open(nerve_state_file, 'rb') as pf:
                    self.nerve_state = json.load(pf)
                self.nerve_state['modified'] = nerve_state_modified
                self.port = self.nerve_state.get('membrane_port')
                self.host = self.nerve_state.get('membrane_host')

    def join(self, *args, **kwargs):
        self.quit = True
        time.sleep(0.01)
        Thread.join(self, *args, **kwargs)

    def talk(self, msg):
        if msg.strip():
	    self.q.put(msg.strip())
        return True

    def _speak(self, msg):
        msg = "%s:%s\n" % (
                self.name,
                msg)

        sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM)

        pmsg = "Membrane sending: %s to tcp://%s:%s" % (
                msg.strip(), self.host, int(self.port))
        print(pmsg)
        sock.connect(
                (self.host,
                 int(self.port)))
        sock.sendall(msg)
        sock.close()

    def _talk(self):
        while not self.quit:
            while not self.q.empty():
                try:
                    self.read_nerve_state()
                    msg = self.q.get()
                    self._speak(msg)
                    self.q.task_done()
                except:
                    print("Error while talking to tcp://%s:%s" % (
                        self.host, self.port))
            time.sleep(0.001)
        msg = "QUIT"
        try:
            self._speak(msg)
        except:
            pass
        return True

    def hostname(self):
        ''' Return hostname of system. '''
        if not self.hostname:
            self.hostname = str(socket.gethostbyaddr(
                socket.gethostname())[0]).split('.')[0]
            return self.hostname
        return self.hostname

if __name__ == '__main__':
    cm = Membrane("XBOX1_CONTROLLER")
    cm.start()
    cm.talk("testing 123..")
    time.sleep(0.1)
    cm.talk("testing 1234..")
    time.sleep(0.1)
    cm.join()
