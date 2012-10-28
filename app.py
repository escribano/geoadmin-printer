import datetime
import hashlib
import os
import subprocess
import simplejson as json
from urlparse import urlparse

from flask import Flask, abort, redirect, render_template, request, jsonify, Response, url_for


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
    height = int(request.args.get('h', 450))
    width = int(request.args.get('w', 600))
    print height, width
    if (height > 1000 and width > 1600):
        return Response("Bad request", status=400)   

    cb = request.args.get('cb', None)
    
    if url and "geo.admin.ch" in url:
        r = "&".join([url,"width=%s" % width, "height=%s" %height])
        url_hash = hashlib.md5(r).hexdigest()
        filename = 'map-%s.jpeg' % url_hash
        
        outfile = os.path.join(MEDIA_ROOT, 'downloads',filename)
        image = os.path.join(MEDIA_URL, 'downloads',filename)
        
        if not os.path.exists(outfile):
            params = [PHANTOM, SCRIPT, url, outfile, str(width), str(height)]
        
            exitcode = subprocess.call(params)
            if exitcode != 0:
                return Response("Internal error", status=500)   
            
        image_url =  url_for('static', filename=os.path.join('downloads',filename), _external=True)
        if cb:
            data = {
                'image'  : image_url,
                'width':  width,
                'height': height
            }
            js = "%s( %s)" %  (cb, json.dumps(data))

            return Response(js, status=200, mimetype='application/json')
        return redirect(image_url)


            
    abort(404)

if __name__ == '__main__':
    # run the application
    app.run()