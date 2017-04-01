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


import Image
import os, sys
import pickle
import pygame
import random
import shutil

def classify_image(art_object):
    colors = {}
    for color in  pygame.color.THECOLORS:
        colors[color] = pygame.color.THECOLORS[color]
    #print(colors)

    creator = art_object.split('/')[2]
    img = Image.open(art_object)
    max_x, max_y = img.size
    pix = img.load()

    image_score  = {}
    for z in range(0,10):
        k = {}
        try:
            a_r, a_g, a_b = pix[int(random.random() * max_x), int(random.random() * max_y)]
        except:
            a_r, a_g, a_b = 255,255,255

        for color in colors:
            c_r, c_g, c_b, c_a = [i for i in colors[color]]
            t = abs(c_r-a_r) + abs(a_g-c_g) + abs(a_b-c_b)
            k[t] = color
        if not k[min(k.keys())] in image_score:
            image_score[k[min(k.keys())]] = 0
        else:
            image_score[k[min(k.keys())]] += 1
    return([k for k,v in image_score.iteritems() if v == max(image_score.values())][0])




def main(arg):


    for j in range(10):
        if not os.path.isfile("art_color_%i.pickle" % j):
            classifications = {}
            with open('all_images.txt', 'r') as fh:
                    data = fh.read()
                    for art_object in data.split():
                        t = {}
                        for i in range(100):
                            res = classify_image(art_object)
                            if not res in t:
                                t[res] = 0
                            else:
                                t[res]+=1
                        print(t, art_object)
                        classifications[art_object] = t
                        pickle.dump(classifications, open("art_color_%i.pickle" %j, "wb" ) )


if __name__ == "__main__":
    main(sys.argv)

