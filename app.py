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
    r = requests.get('http://fixie:YpcpuxmrFDMenhX@54.173.229.200:80', proxies=proxyDict)
    return 'From Fixie'

# @app.route('/next')
# def next():

if __name__ == '__main__':
   app.run(debug=True)

