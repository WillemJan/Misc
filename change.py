#!/usr/bin/env python

from fe2_nl import app
from flask import render_template
import os
import git
import datetime
import sys

@app.route('/change')
@app.route('/change/')

def changelog():
    repos_home=os.path.abspath(os.path.dirname(__file__)+"/../")
    git_handler=git.Repo(repos_home)
    ret_str=""
    logs=git_handler.log()
    for item in logs:
        ret_str+=datetime.datetime(*item.committed_date[:6]).strftime("%Y-%m-%d %H:%M")+" "
        ret_str+=item.message+"\n"
    return(render_template("changelog.html", changelog=ret_str, domain_prefix="www", domain_suffix="fe2.nl"))
