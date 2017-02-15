#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright © 2013 Willem Jan Faber (http://www.fe2.nl) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
* Neither the name of “Fe2“ nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
