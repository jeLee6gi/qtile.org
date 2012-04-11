#!/usr/bin/env python

import cherrypy
import jinja2
import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from pygments_extension import PygmentsExtension

## Setup our jinja template loader
root = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(os.path.join(root, 'templates')),
    extensions=[PygmentsExtension])


## A simple app that serves templates based on the URL path
class QtileDotOrg(object):
    @cherrypy.expose
    def default(self, *path, **kwargs):
        path = '/'.join(path) or 'index'
        try:
            template = env.get_template('{0}.html'.format(path))
        except TemplateNotFound:
            template = env.get_template('404.html')
        return template.render()

## Monkeypatch for Heroku
## See: https://bitbucket.org/cherrypy/cherrypy/issue/1100/cherrypy-322-gives-engine-error-when
from cherrypy.process import servers
def fake_wait_for_occupied_port(host, port): return
servers.wait_for_occupied_port = fake_wait_for_occupied_port

## Set the config and it's time to rock 'n roll!
cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': int(os.environ.get('PORT', 8080)),
    })

cherrypy.quickstart(QtileDotOrg(), config={
    '/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(root, 'static/img/favicon.ico'),
        },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(root, 'static'),
        }
    })
