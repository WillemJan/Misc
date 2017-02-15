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


import sys, os

from cv2.cv import *

def detectObjects(image):
    grayscale = CreateImage((image.width, image.height), 8, 1)
    CvtColor(image, grayscale, CV_BGR2GRAY)

    storage = CreateMemStorage(0)
    #ClearMemStorage(storage)
    EqualizeHist(grayscale, grayscale)
    cascade = Load('ades/haarcascade_frontalface_default.xml', (1,1))
    faces = HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, CV_HAAR_DO_CANNY_PRUNING, (50,50))

    if faces:
        for f in faces:
            print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))

def main():
    image = LoadImage(sys.argv[1]);
    detectObjects(image)


import shutil

if __name__ == "__main__":
    hc = Load("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
    hcp = Load('haarcascade_frontalface_default.xml')

    for f in os.listdir('/home/aloha/remote/pruts.nl/home/aloha/fmale/classified/'):
        try:
            img = LoadImage("/home/aloha/remote/pruts.nl/home/aloha/fmale/classified/"+f, CV_LOAD_IMAGE_GRAYSCALE)
        except:
            continue
        '''
        faces = HaarDetectObjects(img, hc, CreateMemStorage())
        if not os.path.isdir('/home/aloha/c/d/'+str(len(faces))):
            os.mkdir('/home/aloha/c/d/'+str(len(faces)))
        if len(faces) >= 1:
            a,b = faces[0]
            if b>30:
                shutil.copyfile('/home/aloha/remote/pruts.nl/home/aloha/classified/'+ f, '/home/aloha/c/d/'+str(len(faces))+'/'+f)
        '''

        faces = HaarDetectObjects(img, hcp, CreateMemStorage(),  1.2, 2, CV_HAAR_DO_CANNY_PRUNING, (50,50))
        if faces:
            a,b = faces[0]
            if b>15:
                if not os.path.isdir('/home/aloha/c/p/'+str(len(faces))):
                    os.mkdir('/home/aloha/c/p/'+str(len(faces)))
                shutil.copyfile('/home/aloha/remote/pruts.nl/home/aloha/classified/'+ f, '/home/aloha/c/p/'+str(len(faces))+'/'+f)
                for p in faces:
                    print("%s : " % (f), p[0], p[1])
            else:
                shutil.copyfile('/home/aloha/remote/pruts.nl/home/aloha/classified/'+ f, '/home/aloha/c/p/20/'+f)
        else:
            shutil.copyfile('/home/aloha/remote/pruts.nl/home/aloha/classified/'+ f, '/home/aloha/c/p/0/'+f)

