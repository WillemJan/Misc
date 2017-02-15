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

import sys
import time

import analyse
import numpy
import pyaudio
import random

from ctypes import *

from leds import LEDcontroll



chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 0.2

def record_sample():
    # This basicly is the record.py as found in the example directory for pyaudio

    #<stackoverflow>
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    #</stackoverflow>

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        input_device_index = 1,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)
    except:
        return
    raw_sample = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        try:
            data = stream.read(chunk)
            raw_sample.append(data)
        except:
            pass
	stream.stop_stream()
	stream.close()
	p.terminate()
	return(raw_sample)


def main():
    volume_array = []
    prev_state = "down"
    l = LEDcontroll()
    while True:
        raw_sample_data = record_sample()
        base_volume_established = False
        if raw_sample_data:
            for raw_sample in raw_sample_data:
                sample = numpy.fromstring(raw_sample, dtype=numpy.int16)
                volume_array.append(analyse.loudness(sample))

            if len(volume_array) > 10:
                base_volume_established = True

            if base_volume_established:
                for i in range(0, len(volume_array) - 10):
                    volume_array.pop(0)
                current_input = [int(abs(i - sum(volume_array)/10)*10) for i in volume_array]

                print(current_input)

                if current_input[0] > current_input[9] and current_input[0] > current_input[4] and not prev_state == "up" and current_input[0]-current_input[4] > 3:
                    print('up', current_input[4]-current_input[0])
                    prev_state = "up"
                    l.spaceship_min()
                    if current_input[0]-current_input[4] > 4:
                        l.flip_painting()
                    if current_input[0]-current_input[4] > 6:
                        l.flip_robot()
                        l.painting_min(1, rnd=True)
                        l.spaceship_min()

                if current_input[0] < current_input[9] and current_input[0] < current_input[4] and not prev_state == "down" and current_input[4]-current_input[0] > 3:
                    print('down', current_input[0]-current_input[4])
                    prev_state = "down"
                    l.spaceship_min()
                    if current_input[4]-current_input[0] > 4:
                        l.flip_painting()
                    if current_input[4]-current_input[0] > 6:
                        l.flip_robot()
                        l.painting_min(1, rnd=True)
                        l.spaceship_min()

                if current_input[0] < current_input[9] and current_input[0] < current_input[4]:
                    prev_state = "down"
                if current_input[0] > current_input[9] and current_input[0] > current_input[4]:
                    prev_state = "up"


                if abs(current_input[-1] - current_input[-2]) > 2:
                    if random.random() < 0.5:
                        l.spaceship_min(2, s=0.002)
                    else:
                        l.spaceship_max(2, s=0.002)
                if current_input[-1] > 20:
                    if random.random() > 0.5:
                        l.painting_max()
                    else:
                        l.spaceship_max()
                if current_input[-1] > 30:
                    l.painting_max()
                    l.spaceship_max()
                    for i in range(10):
                        l.flip_robot()

if __name__ == '__main__':
    main()
