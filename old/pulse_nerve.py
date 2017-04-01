#!/usr/bin/env python

import time
import os
import json

from pulsectl import Pulse, PulseLoopStop

import cell

class PulseNerve():
    quit = False
    def __init__(self, cm):
	self.pulse = Pulse()
	self.cm = cm

	self.pulse.event_mask_set('all')
	self.pulse.event_callback_set(self.state_change)
	self.pulse.event_listen(timeout=10)


    def run(self):
        while not self.quit:
            time.sleep(0.1)

    def state_change(self, ev):
        #psil = self.pulse.sink_input_list()
        #props = [i.proplist for i in psil]
        print(ev.index, dir(ev.facility), ev.t)
        #raise PulseLoopStop

if __name__ == "__main__":

    name = os.path.basename(__file__)
    name = name.replace('_nerve.py', '')
    cm = cell.Membrane(name)
    cm.start()
    cm.talk("BOOT")

    pulse_nerve = PulseNerve(cm)
    pulse_nerve.run()

    cm.join()
