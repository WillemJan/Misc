#!/usr/bin/python

import os
from wsgiref.handlers import CGIHandler

from flask import Flask
from flask import request, abort, redirect, url_for, jsonify, escape

import urllib2
import json
import sys

from pprint import pprint


sys.path.append(os.path.dirname(__file__))
from lod.freebase import Freebase
from lod.dbpedia import DBPedia
from lod.isbn import Isbn

application = Flask("dbpedia")
application.debug = True

@application.route('/')

@application.route('/isbn:<path:identifier>')
@application.route('/ISBN:<path:identifier>')

@application.route('/dbp:<path:identifier>')
@application.route('/DBP:<path:identifier>')

@application.route('/fb:/<path:identifier>')
@application.route('/fb:<path:identifier>')
@application.route('/FB:/<path:identifier>')
@application.route('/FB:<path:identifier>')


def lod(identifier = None):
    """<html>
    <div id="dbpedia" style='width:900px;height:200px;border-style:solid;border-width:1px;'>
    <h4 style='text-align:center'><b>DBP:</b> DBPedia</h4>
    <iframe src="http://dev.fe2.nl/DBP:Nasa?label_nl,depiction,comment_nl&mode=html" width=600 height=100 style='float: right' frameborder='0'></iframe><br>
    <a href="http://dev.fe2.nl/DBP:Nasa">http://dev.fe2.nl/DBP:Nasa</a><br>
    <a href="http://dev.fe2.nl/DBP:Nasa?label_nl">http://dev.fe2.nl/DBP:Nasa?label_nl</a><br>
    <a href="http://dev.fe2.nl/DBP:Nasa?label_nl,depiction">http://dev.fe2.nl/DBP:Nasa?label_nl,depiction</a><br>
    <a href="http://dev.fe2.nl/DBP:Nasa?depiction&mode=html">http://dev.fe2.nl/DBP:Nasa?depiction&mode=html</a><br>
    <div>

    <div id="isbn" style='width:900;height:200;margin-top:50px;border-style:solid;border-width:1px'>
    <h4 style='text-align:center'><b>ISBN:</b> Isbn</h4>
    <iframe src="http://dev.fe2.nl/ISBN:9023439155?title" width=600 height=100 style='float: right' frameborder='0'></iframe><br>
    <a href="http://dev.fe2.nl/ISBN:9023439155">http://dev.fe2.nl/ISBN:9023439155</a><br>
    <a href="http://dev.fe2.nl/ISBN:9023439155?title">http://dev.fe2.nl/ISBN:9023439155?title</a><br>
    <a href="http://dev.fe2.nl/ISBN:9023439155?google_title">http://dev.fe2.nl/ISBN:9023439155?google_title</a><br>
    </div>
    
    <div id="freebase" style='width:900;height:200;margin-top:50px;border-style:solid;border-width:1px'>
    <h4 style='text-align:center'><b>FB:</b> FreeBase</h4>
    <iframe src="http://dev.fe2.nl/FB:/en/herman_brood?thumbnail&mode=html" width=600 height=100 style='float: right' frameborder='0'></iframe><br>
    <a href="http://dev.fe2.nl/FB:/en/herman_brood">http://dev.fe2.nl/fb:/en/herman_brood</a><br>
    </div>

    </html>
    """
    if not identifier == None:
        request_lod_source = request.path.split(':')[0][1:]
        if not request.args == None:
            req = dict(request.args)
        else:
            req = None
        if "mode" in req:
            if "html" == str(req["mode"][0]):
                mode="html"
                req.__delitem__("mode")
            else:
                mode="json"
                req.__delitem__("mode")
        else:
            mode="json"

        if request_lod_source.lower() == "fb":
            fb = Freebase([escape("/"+identifier)], log_path='/tmp', debug=True, backend='pymongo')
            fb.execute()
            data=fb
        elif request_lod_source.lower() == "isbn":
            isbn = Isbn([escape(identifier)], log_path='/tmp', debug=True, backend='pymongo')
            isbn.execute()
            data = isbn
        elif request_lod_source.lower() == "dbp":
            dbp = DBPedia([escape(identifier)], log_path='/tmp', debug=True, backend='pymongo')
            dbp.execute()
            data = dbp
        else:
            return(lod.__doc__)

        if len(data.keys()) > 0:
            if not req == None:
                if len(req.keys()) > 0:
                    for space in data.keys():
                        ret = ""
                        res = {}
                        for name in req.keys()[0].split(','):
                            if name in data[space]:
                                if str(mode) == "json":
                                    res[name] = data[space][name]
                                else:
                                    if data[space][name].lower().find('.jpg') > -1 or \
                                        data[space][name].lower().find('_thumb') > -1 or \
                                        data[space][name].lower().find('.svg') > -1 or \
                                        data[space][name].lower().find('.gif') > -1:
                                        if data[space][name].lower().find('_thumb') > -1:
                                            ret += "<img id='"+str(space+"_"+name)+"' src='"+data[space][name]+"'></img><br>"
                                        else:
                                            ret += "<img id='"+str(space+"_"+name)+"' src='"+data[space][name]+"'></img><br>"

                                    elif data[space][name].find('http://') > -1:
                                        ret += "<a id='"+str(space+"_"+name)+"' href='"+data[space][name]+"'>"+data[space][name]+"</a><br>"
                                    else:
                                        ret += "<div id='"+str(space)+"_"+name+"'>"+ name.split('_')[0].title() + ": </div>" + data[space][name]+"</br>"
                        if mode == "json":
                            return(jsonify(res))
                        else:
                            return(ret)
                return(jsonify(data))
        return()
    return(lod.__doc__)
