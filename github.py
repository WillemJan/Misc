#!/usr/bin/env python

from fe2_nl import app
from flask import render_template
import os
import datetime

import urllib2
import json

USERNAME = "WillemJan"

@app.route('/github')
@app.route('/github/')
def github():
    global USERNAME
    url = urllib2.urlopen("http://github.com/api/v2/json/repos/show/%s" % USERNAME)
    config = json.loads(url.read())
    return(render_template("github.html", config=config, domain_prefix = "www.", domain_suffix = "fe2.nl"))
