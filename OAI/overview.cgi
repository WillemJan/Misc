#!/usr/bin/env python

import os
import sys
import ast
import cgi
import time
import urllib
import pymongo
import hashlib
import datetime

if __name__ == "__main__":

    dbs=ast.literal_eval(urllib.urlopen('http://kbresearch.nl/mongoOAI/').read())


    print("Content-Type: text/html\n\n")
    print('<html><head> <script type="text/javascript" src="/js/jquery/jquery.js"></script><style>div.table { width:23%; float:left; }</style></head>')
    print("<body>")
    print("<div width=100%>")
    print("<div class='table'>Name</div>")
    print("<div class='table'>Identifiers</div>")
    print("<div class='table'>Fullrecords</div>")
    print("<div class='table'>Indexed</div>")
    print("<br style='clear:left;'>")
    print("<br style='clear:left;'>")

    for db in dbs:
        print("<div class='table' id='"+db+"'>"+db+"</div>")
        print("<div class='table' id='"+db+"_total'>&nbsp</div>")
        print("<br style='clear:left;'>")
        print('<script> $("#'+db+'_total").load("/mongoOAI/?q='+db+'&type=total");</script>')
    print("</div>")
    """

    for item in handler.dbHandler["OAI"].collection_names():
        if not item == "system.indexes":
            try:
                print("")
                handler.dbHandler["OAI"][item].ensure_index("status")
                handler.dbHandler["OAI"].command({"reIndex" : item})
                print("<tr><td>")

                new=handler.dbHandler["OAI"][item].find_one("from")

                if new:
                    print("<font color='green'>%s</font>"%(item))
                    print("<font style='font-size: 8px;'>OAI_from : "+new['from']+"</font>")
                else:
                    print("<font color='red'>%s</font>"%(item))
                print("</td><td>")

                new=handler.dbHandler["OAI"][item].find({"status" : "new"}).count()
                finished=handler.dbHandler["OAI"][item].find({"status" : "done"}).count()

                print("%s"%str(new+finished))
                print("</td><td>")

                fin=handler.dbHandler["OAI"][item].find({"status" : "done"}).count()
                if fin>0:
                    print('<a href=?browse&set="%s">%s</a>'%(item,str(fin)))
                else:
                    print("%s"%str(fin))
                print("</td><td>")
                print("0")
                #print("%s"%str((new+finished)-fin))
                print("</td><td>")

                #indexed=handler.dbHandler["OAI"][item].find({"status" : "indexed"}).count()

                #print("%i"%indexed)
                indexed=handler.dbHandler["OAI"][item].find({"status" : "indexed"}).count()
                print(str(indexed))
                print("</td><td>")
                if (new+finished-fin >0):
                    print("<a href=?getFullrecords&set="+item+">getFullrecords</a>")
                print("</td><td>\n")
            except:
                pass
    print("</table><br/><form>")
    print("<input type=submit value='reindex' action='?reindex=true'>")
    print("</form>")
    """
    print("</body>")
    print("</html>")