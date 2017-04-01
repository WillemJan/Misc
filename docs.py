#!/usr/bin/env python

from fe2_nl import app
from flask import render_template
import os
import datetime


@app.route('/docs')
@app.route('/docs/')
def docs():
    domain_prefix = "www."
    domain_suffix = "fe2.nl"
    config = {"docs" : [] }
    config["docs"].append({"url" : "http://flask.pocoo.org/"  , "name" : "Flask", "img" : "http://"+domain_prefix+domain_suffix+"/static/images/flask.png"})
    config["docs"].append({"url" : "http://jinja.pocoo.org/docs/", "name" : "Jinja2", "img" : "http://"+domain_prefix+domain_suffix+"/static/images/jinja.png"})
    config["docs"].append({"url" : "http://theorem.ca/~mvcorks/code/charsets/auto.html", "name" : "Unicode-table", "img" : "http://"+domain_prefix+domain_suffix+"/static/images/unicode.png"})
    return(render_template("docs.html", config=config, domain_prefix = "www.", domain_suffix = "fe2.nl"))
