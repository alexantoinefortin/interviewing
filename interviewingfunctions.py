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

def initializeSessionList(session):
    session['commentGeneral']=[]
    session['overallScore']=[]
    session['commentCognitive']=[]
    session['cognitiveScore']=[]
    session['commentRoleRelated']=[]
    session['rolerelatedScore']=[]
    session['commentCoolness']=[]
    session['coolnessScore']=[]
    session['commentLeadership']=[]
    session['leadershipScore']=[]
    return session

def removeCommentIfEmpty(session, checkStr):
    session[checkStr] = [x for x in session[checkStr] if x not in ['', u'', ' ', u' ']]
    return session

def addReviewsToSession(session, queryResultsLst):
    if len(queryResultsLst)>0:
        session['intervieweeFirstName'] = queryResultsLst[0]['form_elm']['intervieweeFirstName']
        session['intervieweeLastName'] = queryResultsLst[0]['form_elm']['intervieweeLastName']
        session['interviewDate'] = queryResultsLst[0]['form_elm']['interviewDate']
        session = initializeSessionList(session)
        for i in range(len(queryResultsLst)):
            tmpInfo = queryResultsLst[i]['form_elm']
            session['commentGeneral']+=[tmpInfo['commentGeneral']]
            session['overallScore']+=[tmpInfo['overallScore']]
            session['commentCognitive']+=[tmpInfo['commentOneCognitive']]
            session['commentCognitive']+=[tmpInfo['commentTwoCognitive']]
            session['commentCognitive']+=[tmpInfo['commentThreeCognitive']]
            session['commentCognitive']+=[tmpInfo['commentFourCognitive']]
            session['cognitiveScore']+=[tmpInfo['cognitiveScore']]
            session['commentRoleRelated']+=[tmpInfo['commentOneRoleRelated']]
            session['commentRoleRelated']+=[tmpInfo['commentTwoRoleRelated']]
            session['commentRoleRelated']+=[tmpInfo['commentThreeRoleRelated']]
            session['commentRoleRelated']+=[tmpInfo['commentFourRoleRelated']]
            session['rolerelatedScore']+=[tmpInfo['rolerelatedScore']]
            session['commentCoolness']+=[tmpInfo['commentOneCoolness']]
            session['commentCoolness']+=[tmpInfo['commentTwoCoolness']]
            session['commentCoolness']+=[tmpInfo['commentThreeCoolness']]
            session['commentCoolness']+=[tmpInfo['commentFourCoolness']]
            session['coolnessScore']+=[tmpInfo['coolnessScore']]
            session['commentLeadership']+=[tmpInfo['commentOneLeadership']]
            session['commentLeadership']+=[tmpInfo['commentTwoLeadership']]
            session['commentLeadership']+=[tmpInfo['commentThreeLeadership']]
            session['commentLeadership']+=[tmpInfo['commentFourLeadership']]
            session['leadershipScore']+=[tmpInfo['leadershipScore']]
        session = removeCommentIfEmpty(session, 'commentGeneral')
        session = removeCommentIfEmpty(session, 'commentCognitive')
        session = removeCommentIfEmpty(session, 'commentRoleRelated')
        session = removeCommentIfEmpty(session, 'commentCoolness')
        session = removeCommentIfEmpty(session, 'commentLeadership')
    return session

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
    print myentries
    return myentries

def insert_mongo(db, collection, dict_to_insert):
    db[collection].insert_one(dict_to_insert)
