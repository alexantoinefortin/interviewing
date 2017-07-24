"""
Alex-Antoine Fortin
Sunday, July 23rd 2017
Description
Longer and generally ugly function that are nice to hide here
"""
import json, pandas as pd, numpy as np
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

def returnScoreStats(session, checkStr):
    return [
    str(np.min(session[checkStr]))[:5], str(np.nanpercentile(session[checkStr], 25))[:5],
    str(np.mean(session[checkStr]))[:5], str(np.median(session[checkStr]))[:5],
    str(np.nanpercentile(session[checkStr], 75))[:5], str(np.max(session[checkStr]))[:5]]

def addReviewsToSession(session, queryResultsLst):
    if len(queryResultsLst)>0:
        session = initializeSessionList(session)
        for i in range(len(queryResultsLst)):
            tmpInfo = queryResultsLst[i]['form_elm']
            session['commentGeneral']+=[tmpInfo['commentGeneral']]
            session['overallScore']+=[float(tmpInfo['overallScore'])]
            session['commentCognitive']+=[tmpInfo['commentOneCognitive'], tmpInfo['commentTwoCognitive'], tmpInfo['commentThreeCognitive'], tmpInfo['commentFourCognitive']]
            session['cognitiveScore']+=[float(tmpInfo['cognitiveScore'])]
            session['commentRoleRelated']+=[tmpInfo['commentOneRoleRelated'], tmpInfo['commentTwoRoleRelated'], tmpInfo['commentThreeRoleRelated'], tmpInfo['commentFourRoleRelated']]
            session['rolerelatedScore']+=[float(tmpInfo['rolerelatedScore'])]
            session['commentCoolness']+=[tmpInfo['commentOneCoolness'], tmpInfo['commentTwoCoolness'], tmpInfo['commentThreeCoolness'], tmpInfo['commentFourCoolness']]
            session['coolnessScore']+=[float(tmpInfo['coolnessScore'])]
            session['commentLeadership']+=[tmpInfo['commentOneLeadership'], tmpInfo['commentTwoLeadership'], tmpInfo['commentThreeLeadership'], tmpInfo['commentFourLeadership']]
            session['leadershipScore']+=[float(tmpInfo['leadershipScore'])]
        session = removeCommentIfEmpty(session, 'commentGeneral')
        session = removeCommentIfEmpty(session, 'commentCognitive')
        session = removeCommentIfEmpty(session, 'commentRoleRelated')
        session = removeCommentIfEmpty(session, 'commentCoolness')
        session = removeCommentIfEmpty(session, 'commentLeadership')
        #TODO: remove score with default value & change default value to something ridiculous like 1, 0 or 5
        session['overallScorestat'] = returnScoreStats(session, 'overallScore')
        session['cognitiveScorestat'] = returnScoreStats(session, 'cognitiveScore')
        session['rolerelatedScorestat'] = returnScoreStats(session, 'rolerelatedScore')
        session['coolnessScorestat'] = returnScoreStats(session, 'coolnessScore')
        session['leadershipScorestat'] = returnScoreStats(session, 'leadershipScore')
        #TODO: overall mean
    session['listOfScores'] = ['Overall','Cognitive','Role-related','Coolness','Leadership']
    session['listOfScoresNames'] = ['overallScorestat','cognitiveScorestat','rolerelatedScorestat','coolnessScorestat','leadershipScorestat']
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
