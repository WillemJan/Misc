#!/usr/bin/env python


import cgi, re


form = cgi.FieldStorage()
visitor = { "long" : 0,
            "lat" : 0,
            "date" : "" }
date_chk = re.compile("^\d{2}:\d{2}:\d{2}$")
long_chk = re.compile("^\d+\.*\d*$")


print "Content-Type: text"
print

for item in form.keys():
    if item == "long" or item == "lat":
        if not long_chk.match(form.getvalue(item)) == None:
            visitor[item] = float(form.getvalue(item))
    if item == "date":
        if not date_chk.match(form.getvalue(item)) == None:
            visitor[item] = form.getvalue(item)
if visitor["long"]+visitor["lat"] == 0:
    print("You're not located, too bad..| ")
else:
    visitor["lat"]=str(visitor["lat"])+"%2C"
    print("You're located.|http://www.google.com/uds/modules/elements/mapselement/iframe.html?maptype=roadmap&latlng=%s%s"% (visitor["lat"],visitor["long"]))
