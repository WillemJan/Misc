#!/usr/bin/env python2.7

import sys
import time

import nfc

import cell


class NFC_Nerve():
    def __init__(self, cm):
        self.cm = cm
        initialized = False
        retries = 0
        while not initialized:
            try:
                clf = nfc.ContactlessFrontend('usb')
                msg = "REGISTER:%s" % str(clf)
                self.cm.talk(msg)
                initialized = True
            except:
                msg = "No nfc device found, retries: %i" % retries
                self.cm.talk(msg)
                retries += 1
                time.sleep(1)
                if retries > 10:
                    sys.exit(-1)

        quit = False

        while not quit:
            res = clf.connect(rdwr={'on-connect': self.connected})
            msg = str(time.time())
            msg = "HEARTBEAT:%s" % str(msg)

    def connected(self, tag):
        msg = "TAG:%s" % str(tag)
        self.cm.talk(msg)
        return False

if __name__ == '__main__':
    cm = cell.Membrane("NFC")
    cm.start()
    cm.talk("BOOT")
    nfc_nerve = NFC_Nerve(cm)
