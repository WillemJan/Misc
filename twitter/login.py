#!/usr/bin/env python

##  Mijn ING autologin - mying.py
##  Copyright (C) 2009-2010 Willem Jan Faber
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##  Willem Jan Faber
##  willemjan at fe2 dot nl

import cookielib, urllib, urllib2, string, os

__version__ = "0.01b"

LOGIN = "your_LOGIN_here"
PASSWORD = "your_PASSWORD_here"

# And delete the next line ;)

os._exit(-1)

MIJN_ING_BASEURL = "https://mijn.ing.nl/internetbankieren/SesamLoginServlet"
MIJN_ING_SALDOURL = "https://mijn.ing.nl/mpb/startpaginarekeninginfo.do"

headers = { 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}

cookiejar = cookielib.CookieJar()
urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

request = urllib2.Request(MIJN_ING_BASEURL, None, headers)
url = urlOpener.open(request) 
page = url.read()

data={}
i=0
for line in page.split('\n'):
    if line.strip().startswith("<input") or line.strip().startswith("<form"):
        if line.find('autocomplete=') > -1:
            item=(line.strip().split('name=')[1].split('"')[1])
            if i==0:
                data[item]=LOGIN
            else:
                data[item]=PASSWORD
                break
            i+=1
        
data = urllib.urlencode(data)
request = urllib2.Request(MIJN_ING_BASEURL, data, headers)
url = urlOpener.open(request) 
page = url.read()

request = urllib2.Request(MIJN_ING_SALDOURL, None, headers)
url = urlOpener.open(request)
page = url.read() ## This is the saldo data, you might want to play with this some more ;)

totaal=0.0
for line in page.split('\n'):
    if line.strip().startswith('<td align="right" nowrap>'):
        saldo=(line.strip().split('>')[1].split('<')[0])
        saldo=saldo.replace('.','')
        saldo=saldo.replace(',','.')
        totaal+=string.atof(saldo)
print("Saldo totaal : %.2f" % (totaal))
