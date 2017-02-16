#!/usr/bin/env python

##  solr.py - solr.py
##  Copyright (C) 2010 Willem Jan Faber
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

import urllib, ast, sys, os
import datetime, hashlib

config = """graph_title Numer of Jobs
graph_args --base 1000 -l 0
graph_category jobmonitor
graph_vlabel ICT jobs HBO, Zuid-Holland

"""

DEBUG=False

def get_url(url):
    date_str=datetime.date.today().strftime("%m-%d-%Y")
    dirname="/tmp/ict_jobs/" + date_str
    filename=date_str+"_"+hashlib.md5(url).hexdigest()+".html"
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    try:
        fh=open(dirname+os.sep+filename,"r")
        data=fh.read()
        fh.close()
        return(data)
    except:
        data=urllib.urlopen(url).read()
        fh=open(dirname+os.sep+filename,"w")
        fh.write(data)
        fh.close()
        return(data)
    return("")


def get_ict_jobs(config=False):
    job_urls = {"ictergezocht.nl" : {"url" : "http://www.ictergezocht.nl/it-vacatures/?what=&provinces%5B11%5D=9&levels%5B2%5D=3&flexs%5B0%5D=1&where=den+haag&company=&age=&storesearch=1&submit=ICT+Vacatures+zoeken", "start" : "<h1>", "end" : "vacatures gevonden voor" } ,
                "itjobboard.nl" : { "url" : "http://www.itjobboard.nl/ICT-banen/ICT/Zuid+Holland/alle/0/relevantie/nl/", "start" : 'ResultSearchTerms">', "end" : 'resultaten voor ICT in ZUID AND HOLLAND'},
                "vkbanen.nl" : { "url" : "http://www.vkbanen.nl/overzicht_banen/it--automatisering_banen.jsp?attribuutSector=JSCTR13", "start" : "<li>&nbsp; 1 - 25 van", "end" : "vacatures &nbsp;</li>" } ,
                "nuwerk.nl" : { "url" : "http://www.nuwerk.nl/index.php?action=search&order_by=15&ord=asc&109=111&97=100&102=193&104=63&107=157-158-156-154-133-159-155-118-164", "start" : "Vacatures</span></a><span style='width:128px;color:#FFFFFF; font-weight:bold; font-size:13px;'>(", "end" : ")</span></td>" }
    
    }
    
    for job_site in job_urls.keys():
        if config:
            print("index_" + job_site.replace(".","_")+".label "+job_site.split('.')[0])
            print("index_" + job_site.replace(".","_")+".draw LINE2"+"\n")
        else:
            if DEBUG: print("Getting info for " + job_site)
            sys.stdout.write("index_"+job_site.replace(".","_")+".value ")
        #data=urllib.urlopen(job_urls[job_site]["url"]).read()
            data=get_url(job_urls[job_site]["url"])

            for line in data.split("\n"):
                if (line.find(job_urls[job_site]["start"]) > -1 and line.find(job_urls[job_site]["end"]) > -1):
                    if DEBUG: print(line)
                    sys.stdout.write(line.split(job_urls[job_site]["start"])[1].split(job_urls[job_site]["end"])[0].strip()+"\n")
                    break

    #sys.stdout.write('0\n')

if __name__ == "__main__":
    if sys.argv[-1] == "config":
        for line in config.split('\n'):
            sys.stdout.write(line+"\n")
        get_ict_jobs(config=True)
    else:
        get_ict_jobs()
