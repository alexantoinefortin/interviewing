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
        if self.prefix:
            environ['SCRIPT_NAME'] = self.prefix
            if environ['PATH_INFO'].startswith(self.prefix):
                environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
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
# MONGODB utility functions
def _connect_mongo(conf):
    """ A util for making a connection to mongo """
    with open(conf) as infile:
        conf = json.load(infile)
    if conf['username'] and conf['password']:
        mongo_uri = 'mongodb://{}:{}@{}:{}/{}'.format(conf['username'], conf['password'], conf['host'], conf['port'], conf['db'])
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(conf['host'], conf['port'])
    return conn[conf['db']]

def read_mongo(db, collection, query=''):
    """ Read from Mongo and Store into DataFrame """
    # Make a query to the specific DB and Collection
    cursor = db['interviewing'].aggregate([{"$match": {'id': query}}])
    # Expand the cursor and return all hits for the 'id' in the database
    myentries = list(cursor)
    #print myentries
    return myentries

def insert_mongo(db, collection, dict_to_insert):
    db[collection].insert_one(dict_to_insert)
