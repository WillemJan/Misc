#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright © 2013 Willem Jan Faber (http://www.fe2.nl) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
* Neither the name of “Fe2“ nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import os
import sys
import optparse
import logging
import cPickle 

from random import randrange

__version__ = "1.1"

logging.basicConfig()
log = logging.getLogger("random_ip")
log.setLevel(logging.DEBUG)


class RandomIP():
    lowip = False
    highip = False

    tmp_path = "/tmp/random_ip"

    def __init__(self, lowip=False, highip=False, private="192.168.0", start=0, end=254, history=True):
        self.lowip = lowip
        self.highip = highip
        self.addr = []
        data = []

        if not os.path.isdir(self.tmp_path):
            os.mkdir(self.tmp_path)

        if history:
            if private:
                if os.path.isfile(self.tmp_path + os.sep + private):
                    fh = open(self.tmp_path + os.sep + private, 'r')
                    data = cPickle.load(fh)
                    fh.close()
                    fh = open(self.tmp_path + os.sep + private, 'w')
                else:
                    fh = open(self.tmp_path + os.sep + private, 'w')

            else:
                filename = "all_public"
                fh = open(filename, 'r')
                data = cPickle.load(fh)
                fh.close()
                print(data)

        done = False
        if private:
            i = 254*len(private.split('.'))-1
            if i == 0:
                i = 254
        else:
            i = 254*254*254*254
        while not done:
            i -= 1
            self._generate_ip(private, start, end)
            if not ".".join(self.addr) in data:
                data.append(".".join(self.addr))
                done = True
            else:
                self.addr=[]
                if i < 0:
                    done = True
        if history and not self.addr == []:
            cPickle.dump(data, fh)
            fh.close()

        if self.addr == []:
            cPickle.dump(data, fh)
            fh.close()
            for item in data:
                print(data)

    def _generate_ip(self, private, start, end):
        if not private:
            for i in range(0, 4):
                    self.addr.append(self.random_netblock(start, end, i))
        else:
            for netblock in private.split('.'):
                self.addr.append(netblock)
            for i in range(0+len(self.addr), 4):
                self.addr.append(self.random_netblock(start, end, i))

    def random_netblock(self, start=0, end=254, block=0):
        addr = randrange(start, end, 1)
        if block == 0:
            if addr in [10, 172, 192, 255]:
                return self.__random_netblock__()
        else:
            if addr in [255]:
                return self.__random_netblock__()
        return(str(addr))

    def __repr__(self):
        return(".".join(self.addr))

def main():
    ip = RandomIP()
    sys.stdout.write(str(ip) + "\n")

if __name__ == "__main__":
    main()
