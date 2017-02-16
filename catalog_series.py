#!/usr/bin/env python2.6
import re, string, os, ast, urllib
import tvdb.tvdb_api as tvdb_api
from pprint import pprint
from xml.etree import ElementTree as etree


def generate_serie_previews(self):                                                                                                                                                                          
    for artifact in sorted(self.collection_series_episodes.keys()):                                                                                                                                             
        if "season" in  self.collection_series_episodes[artifact].keys():                                                                                                                                       
            episode=self.collection_series_episodes[artifact]                                                                                                                                                   
            prefix='/prutsgood/'                                                                                                                                                                                                prefix+='preview_'+episode['televison_program_name'].replace(' ', '_')+"_s"+str(episode['season']) + "e"+str(episode['episode'])                                                                    
            name=prefix+'.mpeg'                                                                                                                                                                                 
            encode=subprocess. Popen('mencoder -really-quiet -vf scale=300:200 -of mpeg -ovc lavc -lavcopts vcodec=mpeg1video -oac copy -ss 0:00 -endpos 2:20 "'+artifact+'" -o "'+name+'" 2>/dev/null', shell=True, stdout=subprocess.PIPE)                                                                                                                                                                                        
            info=encode.communicate()[0].strip()                                                                                                                                                                
            encode=subprocess. Popen('ffmpeg -i "' +name+'" -y -f flv -ar 44100 -ab 64 -ac 1 "'+prefix+'.flv" 2>/dev/null', shell=True, stdout=subprocess.PIPE)                                                 
            info=encode.communicate()[0].strip()                                                                                                                                                                
            encode=subprocess. Popen('mv "' +prefix+'.flv" /tmp/prutsgood/data', shell=True, stdout=subprocess.PIPE)                                                                                            
            info=encode.communicate()[0].strip()                                                                                                                                                                
            os.unlink(name)                                                                                                                                                                                     


def get_serie_info(name):
    try:
        file=open("/tmp/"+name.replace(" ", "_")+".xml", "r")
        data=file.read()
        file.close()
        data=etree.fromstring(data)
    except:
        try:
            data=urllib.urlopen("http://www.thetvdb.com/api/GetSeries.php?seriesname="+urllib.quote(name)).read()
            data=("\n".join(data.split("\n")[1:])).lower()
            file=open("/tmp/"+name.replace(" ", "_")+".xml", "w")
            file.write(data)
            file.close()
            data=etree.fromstring(data)
        except:
            data=""
    odata=[]
    name=True
    for item in data.getiterator():
        if len(item.text) >1:
            tagname=item.tag
            et = etree.Element("field",  name="serie_"+tagname)
            if tagname == "seriesname" and name and len(item.text) > 1:
                et = etree.Element("field",  name="seriename")
                et.text = item.text
                name=False
                odata.append(etree.tostring(et))
                print(item.text)
            else:
                et.text = item.text
                odata.append(etree.tostring(et))
    return(odata)



def get_wiki_page(seriename):
    name=""
    for item in seriename.split(" "):
        name+=item.capitalize()+" "
    seriename=name.strip()
    seriename+=" (TV series)"
    seriename=seriename.replace(" ", "_")
    seriename=urllib.quote(seriename)
    try:
        file=open("/tmp/"+seriename+".wiki", "r")
        data=file.read()
        file.close()
    except:
        data=urllib.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+seriename+"&vprop=content&format=json").read()
        file=open("/tmp/"+seriename+".wiki", "w")
        file.write(data)
        file.close()

    known_items=["format", "creator", "first_aired", "starring"]

    list={}
    data=ast.literal_eval(data)
    for name in known_items:
        key=data['query']['pages'].keys()[0]
        for line in data['query']['pages'][key]['revisions'][0]['*'].split('\n'):
            if line.startswith("|"):
                nline=line.split("=")[0].replace("|","").strip()
                if nline.startswith(name):
                    line=line.split("=")[1].strip()
                    for item in line.split("[["):
                        line=(item.replace("]]", "")).strip()
                        line=line.replace("<br \\/>", "")
                        line=line.replace(" with", "")
                        line=line.replace(" and", "")
                        line=line.replace("\\/", "/")
                        if len(line)>1:
                            try:
                                list[name].append(line)
                            except:
                                list[name]=[]
                                list[name].append(line)
    return(list)

media = {}
wierd = ("/" , ".", "-")
tvdb=tvdb_api.Tvdb(banners=True, debug = False, interactive = False, cache =True, actors=True)
i=j=0

config={}

config['magic_parse'] = [
    re.compile('''^.+?(AVI).*$'''),
    re.compile('''^.+?(Matroska).*$'''),
    re.compile('''^.+?(MPEG sequence).*$'''),
    re.compile('''^.+?(Microsoft ASF).*$'''),
    re.compile('''^.+?(ISO Media, MPEG v4 system, version).*$''')
]

config['serie_seasonepisode'] = [
    re.compile('''^.+/(.+)([0-9])([0-9]+)$'''),
    re.compile('''^.+/(.+)([0-9]+)x([0-9]+).*$'''),
    re.compile('''^.+/(.+)s([0-9]+)e([0-9]+).*$'''),
    re.compile('''^.+/(.+)/.+[season].+?([0-9]+).+[episode].+?([0-9]+)*$'''),
    re.compile('''^.+/(.+)-([0-9])([0-9]+).*$''')
]

try:
    f=open("all", "r")
except:
    data=os.popen("find /shared_stuff/video/series/ -exec file '{}' ';' > all").read()
    f=open("all", "r")

record=[]
record.append("<add>\n")
for line in f:
    line=line.strip().replace('/shared_stuff/video/series/','')
    magic=":".join(line.split(":")[1:])
    ok=False
    for r in config['magic_parse']:
        match = r.match(magic)
        if match:
            name=line.split(":")[0].lower()
            for r in config['serie_seasonepisode']:
                if r.match(line.split(":")[0].lower()):
                    #print(r.match(line.split(":")[0]).group(1,2))
                    g=r.match(line.split(":")[0].lower())
                    if g.group(2) and g.group(3):

                        record.append("<doc>\n")
                        name=(g.group(1))
                        name=name.split(" -")[0]
                        name=name.replace(".", " ").strip()
        
                        name=name.replace("lynleymysteries", "inspector lynley mysteries")
                        seriename=name

                        #pprint(get_wiki_page(seriename))

                        season=int(g.group(2))
                        episode=int(g.group(3))

                        seep="%02dx%02d" %(int(season), int(episode))

                        et = etree.Element("field",  name="seep")
                        et.text=seep
                        record.append(etree.tostring(et)+"\n")

                        et = etree.Element("field",  name="filename")
                        print(line)
                        et.text=line.split(":")[0]
                        record.append(etree.tostring(et)+"\n")

                        et = etree.Element("field",  name="media_type")
                        et.text = "serie"
                        record.append(etree.tostring(et)+"\n")

                        et = etree.Element("field",  name="episodenumber")
                        et.text = str(episode)
                        record.append(etree.tostring(et)+"\n")

                        et = etree.Element("field",  name="seasonnumber")
                        et.text = str(season)
                        record.append(etree.tostring(et)+"\n")

                        

                        try:
                            print(seriename, seep)
                            episode=tvdb[seriename][int(season)][int(episode)]
                        except:
                            print("Eror for "+seriename+seep)
                            break


                        actors=tvdb[seriename]['_actors']
                        
                        for actor in actors:

                            if actor["role"]:
                                et = etree.Element("field",  name="serie_actor")
                                et.text = actor.__str__().split('"')[1]
                                record.append(etree.tostring(et)+"\n")

                                et = etree.Element("field",  name="serie_actor_as")
                                et.text = actor.__str__().split('"')[1] + u" as " + actor["role"]
                                record.append(etree.tostring(et)+"\n")

                                et = etree.Element("field",  name="serie_role")
                                et.text = actor["role"]             
                                record.append(etree.tostring(et)+"\n")
                            else:
                                et = etree.Element("field",  name="serie_actor")
                                et.text = actor.__str__().split('"')[1]
                                record.append(etree.tostring(et)+"\n")


                        for item in episode.keys():
                            if episode[item]:
                                if not item.find("number") > -1:

                                    if item=="filename":

                                        et = etree.Element("field",  name="image")
                                        et.text = episode[item]
                                        record.append(etree.tostring(et)+"\n")

                                        url=episode[item]
                                        try:
                                            f=open("/home/aloha/prutsgood/data/series/banners/"+"/".join(url.split("/")[-2:]),"r")
                                            data=f.read(1)
                                        except:
                                            print("Get banner")

                                            try:
                                                os.mkdir("/home/aloha/prutsgood/data/series/banners/"+url.split("/")[-2])
                                            except:
                                                pass
                                            f=open("/home/aloha/prutsgood/data/series/banners/"+"/".join(url.split("/")[-2:]),"w")
                                            data=urllib.urlopen(url).read()
                                            f.write(data)
                                            f.close()
                                    elif item=="gueststars":
                                        for gueststar in episode[item].split("|"):
                                            et = etree.Element("field",  name=item)
                                            et.text=gueststar
                                            record.append(etree.tostring(et)+"\n")
                                    elif item=="seriename":
                                        et = etree.Element("field",  name="seriename")
                                        et.text = episode[item]
                                        record.append(etree.tostring(et)+"\n")
                                    elif item=="writer":
                                        for writer in (episode[item].split("|")):
                                            if len(writer)>1:
                                                et = etree.Element("field",  name="writer")
                                                et.text = writer
                                                record.append(etree.tostring(et)+"\n")
                                    elif item=="director":
                                        for director in (episode[item].split("|")):
                                            if len(director)>1:
                                                et = etree.Element("field",  name="director")
                                                et.text = director
                                                record.append(etree.tostring(et)+"\n")
                                    else:
                                        et = etree.Element("field",  name=item)
                                        et.text=episode[item]
                                        record.append(etree.tostring(et)+"\n")

                        for item in get_serie_info(seriename):
                            record.append(item+"\n")

                        et = etree.Element("field", name="file_metadata")

                        if not line.find("'") > -1:
                            data = ("mplayer  -identify  -frames 0 '"+line.split(":")[0]+"' 2>/dev/null |grep '^ID_'")
                        else:
                            data = ("mplayer  -identify  -frames 0 \""+line.split(":")[0]+"\" 2>/dev/null |grep '^ID_'")
                        data = os.popen(data).read()
                        et.text = data
                        record.append(etree.tostring(et)+"\n")
                        record.append("</doc>\n")
                        break

record.append("</add>\n")
                
data=[]
out=open("all.xml","w")
for line in record:
    out.write(line)
    data.append(line)
out.close()
print("open all.xml")
