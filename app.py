# app.py
import os, requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # return 'Hello from Python!'
    proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }
    r = requests.get('www.google.com', proxies=proxyDict)
    return r

# @app.route('/next')
# def next():

if __name__ == '__main__':
   app.run(debug=True)

