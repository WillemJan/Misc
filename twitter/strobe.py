#!/usr/bin/python

import re, time
from webgrabber import webgrab

grabber=webgrab()
grabber.setReferrer('http://www.xmas4all.net/2007/nl/index.asp')

cookiejar = ['ASPSESSIONIDSSCSBTDQ=FHDKMEGAPMBIHDKINBEPMFFD;', 
			 'ASPSESSIONIDSSCSBTDQ=KOCKMEGAAENMIEFDMEMHHGAL;',
			 'ASPSESSIONIDSSCSBTDQ=AJDKMEGAHGPBDOKLHBDPDOFO;',
			 'ASPSESSIONIDSSCSBTDQ=DJDKMEGABFCFAOJCIGHPDJJI;']

grabber.setCookie('ASPSESSIONIDSSCSBTDQ=FHDKMEGAPMBIHDKINBEPMFFD;')
#grabber.setCookie('ASPSESSIONIDSSCSBTDQ=FDBKMEDCN;')
#grabber.setCookie('ASPSESSIONIDSSCSBTDQ=KOCKMEGAAENMIEFDMEMHHGAL;')

pointer = 0
def rotateCookie():
	print pointer
	global pointer
	currentcookie = cookiejar[pointer]
	print "Current cookie:" ,currentcookie
	grabber.setCookie(currentcookie)
	if pointer == len(cookiejar) -1:
		global pointer
		pointer = 0
	pointer += 1

# Fetch
number = 0
print "grabber"
def grabMain():
	global number
	grabber.grab('http://www.xmas4all.net/2007/nl/index.asp')
	data = grabber['data']
	link = re.match(".*sw2.asp.*", data)
	print "-"*80
	start = data.find('sw2.asp')
	number = data[start+10:start+20]
	number = number.split('&')[0]
grabMain()
print "NUMBER:", number

### Cookie: 
#print "Cookie:", grabber['cookie']
count = 0

def turnSwitch(number=number, switch='1', value='1'):
	global count
	count += 1
	grabber.grab('http://www.xmas4all.net/2007/scripts/sw2.asp?g=%s&ch=%s&v=%s'% (number, switch, value))
	d =  grabber['data'].split()[13:-2]
	if d[0] == 'ok':
		print "CLICK!:", count
		if len(d) > 3:
			if d[-1][-3:].strip() == ":-(":
				print "ERROR!", ' '.join(d)
				time.sleep(30)
			print "JAVASCRIPT: ", ' '.join(d)
			grabMain()
		if d[-1][-3:].strip() == ":-(":
			print "ERROR!", ' '.join(d)
			print "ROTATING!!!!!!! WOOT!"
			rotateCookie()
			grabMain()
			time.sleep(1)
		print "HMMM:", ' '.join(d)
	else:
		print "ERROR:", ' '.join(d)
		time.sleep(15)

def switchOn(number=number, switch='1'):
	turnSwitch(number=number, switch=switch, value='1')

def switchOff(number=number, switch='1'):
	turnSwitch(number=number, switch=switch, value='0')
	
def allOn():
	for i in range(8):
		switchOn(number, i)

def allOff():
	for i in range(8):
		switchOff(number, i)


for i in range(1000):
	for i in range(10):
		switchOn(number, 8)
		switchOn(number, 1)
		switchOn(number, 6)
		switchOff(number, 8)
		switchOff(number, 1)
		switchOff(number, 6)
	
