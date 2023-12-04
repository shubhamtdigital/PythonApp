# app.py
import os, requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Python!'

@app.route('/next')
def next():
    proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }
    r = requests.get('http://fixie:YpcpuxmrFDMenhX@velodrome.usefixie.com:80', proxies=proxyDict)
    return 'From Fixie'

if __name__ == '__main__':
   app.run(debug=True)

