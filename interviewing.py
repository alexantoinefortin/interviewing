"""
Alex-Antoine Fortin
Sunday, July 23rd 2017
Description
Web-app to record feedback about a candidate met during an interview at AmFam
"""
import flask, os, json
from pymongo import MongoClient
from datetime import date
from flask import Flask, session, render_template, redirect, url_for, abort, request
import interviewingfunctions as f

app = Flask(__name__)

#secret maker
os.urandom(24)
app.config['SECRET_KEY'] = '\xe0V7\x08C\x1a\x1c\x81c\xa7\xd7o\xcbo\x02u\x1a\x90\xf6\xb0\x8cT\xf4\xa5' # change that

@app.route('/interviewing', methods=['GET'])
def index():
    #It's the user's first visit to the website
    print 'This is a GET request'
    #f.loadToForm(session)
    if 'progress_count' not in session:
        session['progress_count']=0
    print session
    return render_template( 'interviewing.html',
                            Progress=session['progress_count'],
                            DisplayName='Interviewing')

@app.route('/interviewing', methods=['POST'])
def interviewing():
    global session
    print 'This is a POST request. Count:{}.'.format(session['progress_count'])
    print flask.request.form
    session = f.addToSession(session, flask.request.form)
    if 'next_button' in flask.request.form:
        session['progress_count']+=1
        return redirect(url_for('index'))
    elif 'prev_button' in flask.request.form:
        session['progress_count']= session['progress_count'] - 1
        return redirect(url_for('index'))
    elif 'submit_button' in flask.request.form:
        session.pop('progress_count', None) # don't want to log that
        return redirect(url_for('thankyou'))

@app.route('/interviewing/thankyou', methods=['GET'])
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

@app.route('/interviewing/hiringmanager', methods=['GET'])
def getHiring():
    print "This is a GET request on hiringmanager"
    session.clear()
    return render_template('hiringGET.html', DisplayName='Interviewing')

@app.route('/interviewing/hiringmanager', methods=['POST'])
def postHiring():
    print "This is a POST request on hiringmanager"
    db = f._connect_mongo('config')
    query = flask.request.form.get('intervieweeFirstName')+flask.request.form.get('intervieweeLastName')+flask.request.form.get('interviewDate')
    query = query.lower().strip()
    queryResultsLst = f.read_mongo(db, 'interviewing', query)
    session.clear() # We are done with this information
    # Add review to session
    sess = f.addReviewsToSession(session, queryResultsLst)
    print sess
    return render_template('hiringPOST.html', DisplayName='Interviewing',
    sess=sess)

# SERVING
if __name__ == '__main__':
    app.run(threaded=True)
