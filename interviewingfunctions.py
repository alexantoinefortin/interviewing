"""
Alex-Antoine Fortin
Sunday, July 23rd 2017
Description
Longer and generally ugly function that are nice to hide here
"""
import json, pandas as pd
from pymongo import MongoClient

def loadToForm(session):
    return 0

def addToSession(session, flaskform):
    if 'evaluatorName' in flaskform:
        session['evaluatorName'] = flaskform.get('evaluatorName').strip()
        session['userID'] = flaskform.get('userID').strip()
        session['intervieweeFirstName'] = flaskform.get('intervieweeFirstName').strip()
        session['intervieweeLastName'] = flaskform.get('intervieweeLastName').strip()
        session['intervieweeRole'] = flaskform.get('intervieweeRole').strip()
        session['interviewDate'] = flaskform.get('interviewDate').strip()
        session['commentGeneral'] = flaskform.get('commentGeneral').strip()
        session['overallScore'] = flaskform.get('slider')
    elif 'commentOneCognitive' in flaskform:
        session['commentOneCognitive'] = flaskform.get('commentOneCognitive').strip()
        session['commentTwoCognitive'] = flaskform.get('commentTwoCognitive').strip()
        session['commentThreeCognitive'] = flaskform.get('commentThreeCognitive').strip()
        session['commentFourCognitive'] = flaskform.get('commentFourCognitive').strip()
        session['cognitiveScore'] = flaskform.get('slider')
    elif 'commentOneRoleRelated' in flaskform:
        session['commentOneRoleRelated'] = flaskform.get('commentOneRoleRelated').strip()
        session['commentTwoRoleRelated'] = flaskform.get('commentTwoRoleRelated').strip()
        session['commentThreeRoleRelated'] = flaskform.get('commentThreeRoleRelated').strip()
        session['commentFourRoleRelated'] = flaskform.get('commentFourRoleRelated').strip()
        session['rolerelatedScore'] = flaskform.get('slider')
    elif 'commentOneCoolness' in flaskform:
        session['commentOneCoolness'] = flaskform.get('commentOneCoolness').strip()
        session['commentTwoCoolness'] = flaskform.get('commentTwoCoolness').strip()
        session['commentThreeCoolness'] = flaskform.get('commentThreeCoolness').strip()
        session['commentFourCoolness'] = flaskform.get('commentFourCoolness').strip()
        session['coolnessScore'] = flaskform.get('slider')
    elif 'commentOneLeadership' in flaskform:
        session['commentOneLeadership'] = flaskform.get('commentOneLeadership').strip()
        session['commentTwoLeadership'] = flaskform.get('commentTwoLeadership').strip()
        session['commentThreeLeadership'] = flaskform.get('commentThreeLeadership').strip()
        session['commentFourLeadership'] = flaskform.get('commentFourLeadership').strip()
        session['leadershipScore'] = flaskform.get('slider')
    return session

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

def read_mongo(db, collection, query={}):
    """ Read from Mongo and Store into DataFrame """
    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    print "cursor:{}\n".format(cursor)
    # Expand the cursor and construct the DataFrame
    #print "listcursor: {}".format(list(cursor)[0]['customer'])
    cust_dict = list(cursor)[0]
    print "cust_dict:{}\n".format(cust_dict)
    cust_info =  pd.Series(cust_dict)
    print cust_info.dtypes
    #cust_info.columns = [col.encode('ascii', 'ignore') for col in cust_info if col not in ['_id']]
    return cust_info

def insert_mongo(db, collection, dict_to_insert):
    db[collection].insert_one(dict_to_insert)
