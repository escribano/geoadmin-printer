import datetime
import hashlib
import os
import subprocess

from flask import Flask, abort, redirect, render_template, request

# app configuration
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(APP_ROOT, 'static')
MEDIA_URL = '/static/'
PHANTOM = 'phantomjs'
SCRIPT = os.path.join(APP_ROOT, 'screenshot.js')

# create our flask app and a database wrapper
app = Flask(__name__)
app.config.from_object(__name__)

app.debug = True


@app.route('/')
#@app.route('/<name>')
def index():
    return render_template('default.html')

@app.route('/print')
def printer():
    
    url = request.args.get('url')
    if url and "geo.admin.ch" in url:
        url_hash = hashlib.md5(url).hexdigest()
        filename = 'bookmark-%s.png' % url_hash
        
        outfile = os.path.join(MEDIA_ROOT, 'downloads',filename)
        params = [PHANTOM, SCRIPT, url, outfile]

        exitcode = subprocess.call(params)
        if exitcode == 0:
            image = os.path.join(MEDIA_URL, 'downloads',filename)
            return redirect(image)
            
    abort(404)

if __name__ == '__main__':
    # create the bookmark table if it does not exist
    

    # run the application
    app.run()