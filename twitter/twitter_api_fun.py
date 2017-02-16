#!/usr/bin/env python3.1

import urllib.request, json, time, hashlib, os

known = []

if os.path.isfile('known'):
    fh = open('known' , 'r')
    for url in fh.read():
        known.append(url)
else:
    fh = open('known' , 'w')
    fh.close()


while 1:

    raw_data=False
    try:
        raw_data = urllib.request.urlopen('http://api.twitter.com/1/statuses/public_timeline.json').read().decode('utf-8')
    except:
        time.sleep(60)
    if raw_data:
        data = json.loads(raw_data)
        i=0
        for item in data:
            raw_data=""
            url=item['user']['profile_image_url'].replace('_normal','')
            if not url in known:
                print('Getting url : ' +url)
                known.append(url)

                fh=open('known','a')
                fh.write(url+'\n')
                fh.close()
                try:
                    raw_data = urllib.request.urlopen(url).read()
                except:
                    print("Failed")
                print(len(raw_data))
                print(50000)
                if len(raw_data) > 50000:
                    i+=1

                    if url.endswith('.png'):
                        ext = ".png"
                    else:
                        ext = ".jpg"
                    fh=open(hashlib.md5(item['user']['name'].encode('ascii','ignore')).hexdigest()+ext,'wb')
                    fh.write(raw_data)
                    fh.close()
                    print("Got " + str(i))

