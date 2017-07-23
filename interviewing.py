"""
Alex-Antoine Fortin
Sunday, July 23rd 2017
Description
Web-app to record feedback about a candidate met during an interview at AmFam
"""
import flask, os.path, imp
from datetime import date
from flask import Flask, render_template, redirect, url_for, abort
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
@app.route('/interviewing', methods=['GET','POST'])
#@auth.login_required
def interviewing():
    return render_template('interviewing.html')

# SERVING
if __name__ == '__main__':
    app.run(threaded=True)
