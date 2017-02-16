#!/usr/bin/python


from pprint import pprint
import pickle, gzip, BeautifulSoup, urllib
import codecs 
from operator import itemgetter
import sys, hashlib
streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)


common_word_list=[]

clean_list = ",.<>/?;:'\'\\{}[]=-_+)(*&^%$#@!\"`~ "

lst={}

person_list=[ "hargmc", "locuta" ]
person_count=0
deny_list=[]
for person in person_list:

    for j in range(1,20):
        c=0 
        path="cache/"
        try:
            f=open(path+hashlib.md5(person+str(j)).hexdigest(), "r")
            data=f.read()
            f.close()
        except:
            data=urllib.urlopen('http://twitter.com/'+person+'?max_id=6236276223&page='+str(j)+'&twttr=true').read()
            f=open(path+hashlib.md5(person+str(j)).hexdigest(), "w")
            f.write(data)
            f.close()

        soep=BeautifulSoup.BeautifulSoup(data)
        for item in soep.findAll('span', {'class' : 'entry-content' }):
            for i in item.contents:
                st=(unicode(i.extract()).encode("ascii", "ignore"))
                try:
                    for item in (i.extract().split(' ')):
                        if len(item.strip()) > 3:
                            word=item.strip().lower()
                            if word not in common_word_list:
                                for item in clean_list:
                                    if word.find(item) > -1:
                                        word=word.replace(item, "")
                                if len(word) > 0:
                                    if word not in lst.keys():
                                        lst[word]=0
                                    else:
                                        lst[word]+=1
                except:
                    j-=1



    i=0
    file=open(person, "w")
    for item in (sorted(lst.iteritems(), key=itemgetter(1), reverse=True)):
        if item[1] >1 and item[0].encode('ascii', 'replace') not in deny_list:
            if i==0:
                all=item[1]/100.0
                file.write(item[0]+":100\n")
            else:
                file.write(item[0].encode('ascii', 'replace')+":"+str( item[1]/all)+"\n")
            i+=1
        else:
            if item[1]>4:
                if person_count == 1:
                    print(item[0])
    file.close()

    if person_count == 0:
       for item in (sorted(lst.iteritems(), key=itemgetter(1), reverse=True)):
           deny_list.append(item[0].encode('ascii', 'replace'))
    person_count+=1
