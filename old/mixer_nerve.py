#!/usr/bin/env python

import os
import json
import time
import pigpio
import cell
from pulsectl import Pulse


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


if __name__ == "__main__":

'''
from pulsectl import Pulse

with Pulse('volume-increaser') as pulse:
	for sink in pulse.sink_list():
		print(dir(sink), sink.name, sink.volume, sink.proplist)
'''





    name = os.path.basename(__file__)
    name = name.replace('_nerve.py', '')
    cm = cell.Membrane(name)
    cm.start()
    cm.talk("BOOT")
    initialized = False
    state = {}
    while not initialized:
        pi = pigpio.pi()
        if not pi.connected:
            cm.talk("INIT:FAILED")
            time.sleep(1)
        for i in range(10):
            cm.talk("REGISTER:GPIO")
            time.sleep(0.01)
        initialized = True

    quit = False
    i = 0
    changed = False

    while not quit:
        if changed:
                cm.talk("EVENT:%s" %
                        json.dumps(state))
                changed = False
        else:
            for i in range(32):
                if i in [28, 29]:
                    continue

                val = "%s:%s" % (str(pi.read(i)), str(pi.get_mode(i)))

                if i not in state or not state.get(i) == val:
                    print(val, state.get(i), i)
                    state[i] = val
                    changed = True

        i += 1
        if i % 20 == 0:
            if changed:
                cm.talk("EVENT:%s" %
                        json.dumps(state))
                changed = False

            cm.talk("HEARTBEAT:%s" %
                    str(time.time()))
            time.sleep(0.2)
        time.sleep(0.1)
    cm.join()
