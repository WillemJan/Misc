#!/usr/bin/env python

from fe2_nl import app
from flask import render_template
import os
import datetime


@app.route('/dotfiles')
@app.route('/dotfiles/')

def dotfiles():
    DOTFILES = "/".join(__file__.split('/')[:-1]) + os.sep + "static" + os.sep + "dotfiles"
    config = {}

    for path in os.listdir(DOTFILES):
        if os.path.isdir(DOTFILES + os.sep + path):
            config[path.title()] = {}
            config[path.title()]["config"] = {}
            config[path.title()]["image"] =  "/static/dotfiles/" + path + "/" + path + ".png"
            for config_file in os.listdir(DOTFILES + os.sep + path):
                if not (config_file.endswith('.png') or config_file.endswith('.html')):
                    config[path.title()]["config"][path + "/" + config_file] =  path + "/" + config_file

    return(render_template("dotfiles.html", config=config, domain_prefix = "www.", domain_suffix = "fe2.nl"))
