#!/usr/bin/env python

import logging

from lod import app
from flask import Response
from flask import render_template, request
from flask import globals as g
from werkzeug import Headers

try:
    import json
except:
    import simplejson as json

def log(message, log_level = logging.CRITICAL):
    logging.log(log_level, message)

@app.route('/')
def index(key=None):
    mode = ""
    req = {}

    if request.path.find(':') > -1:
        prefix = request.path.split(':')[0][1:].upper()

        if not request.args == None:
            req = dict(request.args)
        if "mode" in req.keys():
            mode = str(req["mode"][0])
            req.pop("mode")
            if mode == "html":
                pass
            else:
                mode="json"
        else:
            mode = "json"

        keys = req.keys()
        data = {}

        if prefix.lower() == "dbp":
            from LODproxy import dbpedia

            data["data"] = {}
            key = key.replace(' ','_')
            dbp = dbpedia.DBPedia(key)
            data["record"] = dbp.parse()

        if prefix.lower() == "geo":
            from LODproxy import geonames

            geo = geonames.GEOnames(key)
            data["record"] = geo.parse()

        if prefix.lower() == "googleisbn":
            from LODproxy import googleisbn

            gisbn = googleisbn.GOOGLEisbn(key)
            data["record"] = gisbn.parse()

        if prefix.lower() == "sameas":
            from LODproxy import sameas

            key = key.replace('http:/', 'http://')
            same = sameas.SAMEas(key)
            data["record"] = same.parse()


        if len(keys) > 0:
            data["data"] = {}
            for item in keys[0].split(','):
                if not item in ("listkeys", "mode"):
                    if item in data["record"].keys():
                        data["data"][item] = ""
                        data["data"][item] = data["record"][item]
                if item == "listkeys":
                    for item in data["record"].keys():
                        data["data"] = {}
                        data["data"]["keys"]=data["record"].keys()
                    break
        else:
            data["data"] = data["record"]

        if mode == "html":
            return('ok')
        else:
            h = Headers()
            h.add('Content-Type',"application/json")
            return(Response(json.dumps(data["data"]), headers=h))
    else:
        return (render_template('index.html', baseurl=g.BASEURL, modules=g.modules))

#ctx = _request_ctx_stack.top
#return(str(request.path.find(':')))
#return(ctx.url_adapter.path_info)

for module in g.modules:
    app.add_url_rule('/' + module.upper() + ":<path:key>" , module.lower(), index)
    app.add_url_rule('/' + module.lower() + ":<path:key>" , module.lower(), index)
    app.add_url_rule('/' + module + ":<path:key>" , module, index)
