#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Gezelligheid Willem Jan Faber 2013
'''


import os
import glob
import pickle
import hashlib
import sys

#from print import pprint
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


class ArtServer(dict):
    CLASSIFY_PICKLES = '/home/aloha/code/arts/*.pickle'

    def __init__(self, *args, **kwargs):
        # Intro stuff
        self['program_name'] = args[0]
        data = open('arts_server.py', 'r').read()
        self['current_version'] = hashlib.md5(data).hexdigest()
        print('Running `%(program_name)s`, current version %(current_version)s\n' % self)

        # Load and parse images info from www.ibiblio.org.
        for filename in sorted(glob.glob(self.CLASSIFY_PICKLES)):
            # Debug info
            filename_short = filename.split(os.sep)[-1]
            print('Loading file: %s' % filename_short)

            # Acctualy load the pickle
            with open(filename, 'rb') as fh:
                data = pickle.load(fh)
                if not 'artist_names_short' in self.keys():
                    self['artist_names_short'] = sorted([name.split(os.sep)[4] for name in data])

    
    def list_works_by_artistname(self, request):
        if request.matchdict['name'] in self['artist_names_short']:

            return Response('Showing artist: %(name)s works:'
                    % request.matchdict)
        return Response('<font color="red">Unkown artist %(name)s</font>' % request.matchdict)

    def index(self, request):
        return Response('Yep')

    def run(self):
        config = Configurator()

        # route index
        config.add_route('index', '/')
        config.add_view(self.index, route_name='index')

        # route works per artist
        config.add_route('list_works_by_artistname', '/artists/{name}')
        config.add_view(self.list_works, route_name='list_works')

        app = config.make_wsgi_app()
        server = make_server('127.0.0.1', 1338, app)
        server.serve_forever()

if __name__ == '__main__':
    program_name = sys.argv[0].split('.')[0]
    arts_server = ArtServer(program_name)
    arts_server.run()
