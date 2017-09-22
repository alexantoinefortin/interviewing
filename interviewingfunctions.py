"""
Alex-Antoine Fortin
Sunday, July 23rd 2017
Description
Longer and generally ugly function that are nice to hide here
"""
import json, pandas as pd, numpy as np
from pymongo import MongoClient
from wtforms import Form, StringField, validators

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
    try:
        tmp = [x for x in session[checkStr] if x not in ['1','1.0',1,1.0]] # ignore default value
        return [
        str(np.min(tmp))[:5], str(np.nanpercentile(tmp, 25))[:5],
        str(np.mean(tmp))[:5], str(np.median(tmp))[:5],
        str(np.nanpercentile(tmp, 75))[:5], str(np.max(tmp))[:5],
        str(len(tmp))]
    except:
        return ['','','','','','','']

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
    # Removes score with default value
    print "session overallScorestat"
    session['overallScorestat'] = returnScoreStats(session, 'overallScore')
    session['cognitiveScorestat'] = returnScoreStats(session, 'cognitiveScore')
    session['rolerelatedScorestat'] = returnScoreStats(session, 'rolerelatedScore')
    session['coolnessScorestat'] = returnScoreStats(session, 'coolnessScore')
    session['leadershipScorestat'] = returnScoreStats(session, 'leadershipScore')
    try:
        session['totalAverageScore'] = [str(r) for r in np.mean([[float(x) for x in session['overallScorestat']], [float(x) for x in session['cognitiveScorestat']],[float(x) for x in session['rolerelatedScorestat']], [float(x) for x in session['coolnessScorestat']], [float(x) for x in session['leadershipScorestat']]], axis=0)]
    except: # if len(queryResultsLst)==0
        session['totalAverageScore'] = ['','','','','','','']
    #TODO: overall mean
    session['listOfScores'] = ['Overall','Cognitive','Role-related','Coolness','Leadership', 'Total (average)']
    session['listOfScoresNames'] = ['overallScorestat','cognitiveScorestat','rolerelatedScorestat','coolnessScorestat','leadershipScorestat', 'totalAverageScore']
    return session

class RegistrationForm(Form):
    """
    Class to use with wtforms. It makes it easy to validate forms before submiting them.
    """
    sqlValidators = validators.Regexp(regex=r'^[A-Za-z0-9@$%^&+,:\ .]+$', message='Allowed characters are alphanumerics, spaces and @$%^&+,:.')
    evaluatorName = StringField('evaluatorName', [validators.DataRequired(message='Your name is required'), sqlValidators])
    userID = StringField('userID', [validators.Regexp(regex= '^[a-zA-Z][a-zA-Z][a-zA-Z][0-9][0-9][0-9]$', message='UserID must have the format xxx000.'), validators.DataRequired(message='Your userID is required'), sqlValidators])
    intervieweeFirstName = StringField('intervieweeFirstName', [validators.Length(min=2, max=35, message="The interviewee's first name must be between %(min)d and %(max)d characters long."), sqlValidators])
    intervieweeLastName = StringField('intervieweeLastName', [validators.Length(min=2, max=35, message="The interviewee's last name must be between %(min)d and %(max)d characters long."), sqlValidators])
    intervieweeRole = StringField('intervieweeRole', [validators.DataRequired(message='Role interviewed for is required.'), sqlValidators])
    interviewDate = StringField('interviewDate', [validators.Regexp(regex= '^((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))$', message='Date of interview must be a valid date and respect the format MM/DD/YYYY.'), validators.Length(min=10, max=10, message="For the date of interview, make sure that both month and day have 2 digits each (09 instead of 9), and that year has 4 digits (1999 or 2016 instead of 99 or 16)"), validators.DataRequired(message='Date of interview is required.')])

class queryACandidateForm(Form):
    """
    Class to use with wtforms. It makes it easy to validate forms before submiting them.
    """
    sqlValidators = validators.Regexp(regex=r'^[A-Za-z0-9@$%^&+,:\ .]+$', message='Allowed characters are alphanumerics, spaces and @$%^&+,:.')
    intervieweeFirstName = StringField('intervieweeFirstName', [validators.Length(min=2, max=35, message="The interviewee's first name must be between %(min)d and %(max)d characters long."), sqlValidators])
    intervieweeLastName = StringField('intervieweeLastName', [validators.Length(min=2, max=35, message="The interviewee's last name must be between %(min)d and %(max)d characters long."), sqlValidators])
    interviewDate = StringField('interviewDate', [validators.Regexp(regex= '^((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))$', message='Date of interview must be a valid date and respect the format MM/DD/YYYY.'), validators.Length(min=10, max=10, message="For the date of interview, make sure that both month and day have 2 digits each (09 instead of 9), and that year has 4 digits (1999 or 2016 instead of 99 or 16)"), validators.DataRequired(message='Date of interview is required.')])
