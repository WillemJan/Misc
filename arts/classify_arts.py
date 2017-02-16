#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 2013 Willem Jan Faber 
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

