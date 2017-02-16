import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import webhelpers.constants
from home.lib.app_globals import Globals as g

import os
from home.model import get_db, Factsheet
import couchdb

from home.lib.base import BaseController, render

log = logging.getLogger(__name__)

FLAG_PATH="/home/public/country_flags/"

class CountryController(BaseController):
    def index(self):
        return (render('/country.mako'))

    def list(self):
        return (render('/country_list.mako'))

    def get_population(self, id):
        return(g.__grab__.pop("nl"))
        
        #f=g.get_population(g)
        #go=False
        #for l in f.split("\n"):
        #    if (go):
        #        i=0
        #        l=l.strip(" ")
        #        l=l.strip("\n")
        #        if len(l)>0:
        #            if not l.startswith("<"):
        #                l=l.split(" ")[0]
        #                break
        #        if (l.find('</td>') > -1) and (i>1):
        #            go=False
        #    if (l.find('<div align="right">Population:</div>') > -1):
        #        go=True
