# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Python!'

@app.route('/next')
def next():
    return 'Hello from nextPath!'

if __name__ == '__main__':
   app.run(debug=True)

