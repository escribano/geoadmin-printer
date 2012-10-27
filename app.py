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
        filename = 'map-%s.jpeg' % url_hash
        
        outfile = os.path.join(MEDIA_ROOT, 'downloads',filename)
        image = os.path.join(MEDIA_URL, 'downloads',filename)
        
        if os.path.exists(outfile):
            return redirect(image)
        else:
               
            params = [PHANTOM, SCRIPT, url, outfile]

            exitcode = subprocess.call(params)
            if exitcode == 0:
                return redirect(image)
            
    abort(404)

if __name__ == '__main__':
    # run the application
    app.run()