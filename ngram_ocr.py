#!/usr/bin/env python

# N-gram OCR evaluation

#  Succeed hackathon 2014 (Alicante)
#  Willem Jan Faber


#
# To use download http://homepages.inf.ed.ac.uk/lzhang10/ngram.html
# create a file 'out' from training data like so:
#
#  text2ngram -c -n3 ./input_training_data > out
#
# After this step, call the program:
#  export PYTHONIOENCODING=UTF-8
#  python ngram_ocr.py ./ocr_file > output.html
#


import sys
from pprint import pprint
import cgi

nsize = 3
dm = {}
res = {}
inputtxt = sys.argv[1]
fh = open("out1", 'r')
data = fh.read()
print "<hr><br><h1>" + inputtxt + "</h1> "
for line in data.split('\n'):
    if len(line.split(' ')) > 1:
        dm[line.split(' ')[0]] = int(line.split(' ')[1])
fh = open(inputtxt,  'r')
input_text = fh.read()
total_words = 0 
bad_words = 0
good_words = 0
for item in input_text.split(' '):

    if len(item) == nsize:
        #print '\t' + item, dm.get(item)
        res[item] = dm.get(item)
    else:
        j = 0
        for i in range(len(item)):
            if len(item[i:i+nsize]) == nsize:
                j += 1
                if not item in res:
                    res[item] = 0
                if dm.get(item[i:i+nsize]) == None:
                    res[item] = res[item] - 1000
                else:
                    res[item] += dm.get(item[i:i+nsize])
        if item in res:
            res[item] = res[item] / j
            if res[item] < 0:
                print "<font color='red'>" + cgi.escape(item) + "</font>"
                total_words +=1
                bad_words += 1
            else:
                print "<font color='black'>" + cgi.escape(item) + "</font>"
                good_words += 1
                total_words +=1
total = 0
j = 0
for i in res:
    if not res[i] == None:
        j += 1
        total += res[i]
print "<br><b>"
print (total/ j)
print "<br>Total words: " + str(total_words) + "<br>Good words: " + str(good_words) + "<br>Bad words: " + str(bad_words) + " ("
print bad_words / (total_words / 100.0)
print "%)<br><font color='black'>"
if total /j < 0:
    print "<font color='red'>Ocr quality: very bad</font><br>"
if total/j > 0 and total/j < 30: 
    print "<font color='red'>Ocr quality: bad</font><br>"
if total/j > 30 and total/j < 50: 
    print "<font color='green'>Ocr quality: good</font><br>"
if total/j > 50 and total/j < 70: 
    print "<font color='green'>Ocr quality: very good</font><br>"
if total/j > 70:
    print "<font color='green'>Ocr quality: excellent!</font><br>"
print "</font></b><br>"
