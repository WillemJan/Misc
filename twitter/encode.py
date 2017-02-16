#!/usr/bin/env python
import os

f = open("15251.txt")
data=f.read()
data_block={}

i=0
for l in data.split('\n'):
    i+=1
file_length=i
f.close()

#for j in range(0,file_length):
#    i=0
tot=0
max=0
d=(data.split('\n')[0].split(" ")[0])
print(len(d))
seek={}
seek[(d[0:2])]=False
seek["e "]=False

f = open("message.txt")
data=f.read()
w=""
found=0
print(seek)
print("***")
for i in range(len(data.split('\n'))):
     d=data.split('\n')[i].strip()
     for j in d:
         if (j.isalpha() or j=="'"):
             w=w+j
         if (len(w) == 2):
             for item in seek.keys():
                 if item == w and not seek[item]:
                    print(w,i)
                    seek[item]=i
                    found+=1
                    if (found == 2):
                        os._exit(-1)
             w=""
         
'''
a=(sorted(data_block.keys()))
for j in range(len(a)):
    print a[j], (j)
'''
f.close()

