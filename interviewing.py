"""
Alex-Antoine Fortin
Sunday, July 23rd 2017
Description
Web-app to record feedback about a candidate met during an interview at AmFam
"""
from webtools import PrefixMiddleware, run_server  ##Added
import flask, json
import datetime
from pymongo import MongoClient
from flask import Flask, session, render_template, redirect, url_for, request
import interviewingfunctions as f
from interviewingfunctions import RegistrationForm

app = Flask(__name__)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/interviewing') ##Added
with open('config') as infile:
    app.config['SECRET_KEY'] = json.load(infile)['secret']

@app.route('/', methods=['GET'])
def index():
    #It's the user's first visit to the website
    print 'This is a GET request'
    form = RegistrationForm(flask.request.form)
    if 'progress_count' not in session:
        session['progress_count']=0
    print session
    return render_template( 'interviewing.html',
                            Progress=session['progress_count'],
                            DisplayName='Interviewing',
                            sess = session, form=form)

@app.route('/', methods=['POST'])
def interviewing():
    global session
    print 'This is a POST request'
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60) # Session expires after 60 minutes
    flask.session.modified = True # Reset counter for session timeout when set to True
    session = f.addToSession(session, flask.request.form)
    form = RegistrationForm(flask.request.form)
    if 'progress_count' not in session.keys():
        print "progress_count not in session.keys()"
        session['progress_count']=0
        return redirect(url_for('index'))
    elif 'next_button' in flask.request.form and int(session['progress_count'])==0 and form.validate(): # must validate General questions
        print"next_button, progress_count==0, form.validate"
        session['progress_count']+=1
        return redirect(url_for('index'))
    elif 'next_button' in flask.request.form and int(session['progress_count'])!=0 : # unnecessary to validate cognitive, role-related, coolness, and leadership tabs
        session['progress_count']+=1
        return redirect(url_for('index'))
    elif 'prev_button' in flask.request.form:
        session['progress_count']= session['progress_count'] - 1
        return redirect(url_for('index'))
    elif 'submit_button' in flask.request.form:
        session.pop('progress_count', None) # don't want to log that
        session.pop('current_count', None) # don't want to log that
        return redirect(url_for('thankyou'))
    elif 'progress_count' in flask.request.form and int(flask.request.form.get('current_count'))==0 and form.validate(): # used tab to navigate the website from General tab
        session['progress_count'] = int(flask.request.form.get('progress_count'))
        return redirect(url_for('index'))
    elif 'progress_count' in flask.request.form and int(flask.request.form.get('current_count'))==0 and form.validate()==False: # used tab to navigate the website from General tab
        session['progress_count'] = int(flask.request.form.get('current_count'))
        return render_template( 'interviewing.html',
                                Progress=session['progress_count'],
                                DisplayName='Interviewing',
                                sess = session, form=form)
    elif 'progress_count' in flask.request.form and int(flask.request.form.get('current_count'))!=0: # used tab to navigate the website from another tab
        session['progress_count'] = int(flask.request.form.get('progress_count'))
        return redirect(url_for('index'))
    else: # form did not validate
        #session['progress_count']=session['form_did_not_validate_progress']
        print 'form did not validate'
        return render_template( 'interviewing.html',
                                Progress=session['progress_count'],
                                DisplayName='Interviewing',
                                sess = session, form=form)

# handle used to navigate the website using the tabs
@app.route('/<progress_count>', methods=['GET', 'POST'])
def redirect_to_other_page(progress_count):
    try:
        session['progress_count']=int(progress_count)
    except:
        session['progress_count']=0
    return redirect(url_for('interviewing'))

@app.route('/thankyou', methods=['GET'])
def thankyou():
    # post session to DB
    db = f._connect_mongo('config')
    dict_to_insert = {'form_elm':dict(session)}
    dict_to_insert['id'] = dict_to_insert['form_elm']['intervieweeFirstName']+dict_to_insert['form_elm']['intervieweeLastName']+dict_to_insert['form_elm']['interviewDate']
    dict_to_insert['id'] = dict_to_insert['id'].lower().strip()
    print "id is:{}.".format(dict_to_insert['id'])
    f.insert_mongo(db, 'interviewing', dict_to_insert)
    # clear session
    tmp_first = session['intervieweeFirstName']
    session.clear()
    return render_template( 'thankyou.html',
                            DisplayName='Interviewing',
                            IntervieweeName=tmp_first)

@app.route('/hiringmanager', methods=['GET'])
def getHiring():
    print "This is a GET request on hiringmanager"
    session.clear()
    return render_template('hiringGET.html', DisplayName='Interviewing')

@app.route('/hiringmanager', methods=['POST'])
def postHiring():
    print "This is a POST request on hiringmanager"
    if 'back_button' in flask.request.form:
        return redirect(url_for('getHiring'))
    else:
        db = f._connect_mongo('config')
        query = flask.request.form.get('intervieweeFirstName')+flask.request.form.get('intervieweeLastName')+flask.request.form.get('interviewDate')
        query = query.lower().strip()
        queryResultsLst = f.read_mongo(db, 'interviewing', query)
        session.clear() # We are done with this information
        # Add reviews/comments to session
        session['intervieweeFirstName'] = flask.request.form.get('intervieweeFirstName')
        session['intervieweeLastName'] = flask.request.form.get('intervieweeLastName')
        session['interviewDate'] = flask.request.form.get('interviewDate')
        sess = f.addReviewsToSession(session, queryResultsLst)
        return render_template('hiringPOST.html', DisplayName='Interviewing',
        sess=sess)

# SERVING
if __name__ == '__main__':
    run_server(app) ##Added
    #app.run(host='0.0.0.0', threaded=True)
