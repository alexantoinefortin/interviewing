"""
Author: Alex-Antoine Fortin
Thursday, August 10th 2017
Description
Tools used to deploy website conveniently
"""
import cherrypy

class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

def run_server(app, port=5000, host='0.0.0.0'):
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app,'/')
    # Set the configuration of the webserver
    cherrypy.config.update({
    'engine.autoreload.on': True,
    'log.screen': True,
    'server.socket_port': port,
    'server.socket_host': host
    })
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()

def catch(func, handle=lambda e : e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handle(e)
        
