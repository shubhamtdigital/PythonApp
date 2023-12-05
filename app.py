# app.py
import os, requests
from flask import Flask

import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
import socks
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    # return 'Hello from Python!'
    proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }
    r = requests.get('https://www.google.com', proxies=proxyDict)
    return r.text

@app.route('/dbconnect')
def connect():
    # Parse the database URL
db_url = "postgres://ucrol25emqd2ch:p31d791a3fe8bcb5b5102d7b8b43f08ca70ee2cc9d7943c23b4db6b110324346e@ec2-44-205-97-79.compute-1.amazonaws.com:5432/d2r45oj3jf7gs7"
url = urlparse(db_url)

# Set up the proxy settings
proxy_host = 'proxy_host'
proxy_port = 1080
proxy_type = socks.SOCKS5  # Change this based on your proxy type

# Set up the connection parameters
conn_params = {
    'database': url.path[1:],
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port,
}

# Set up the proxy
socks.set_default_proxy(proxy_type, addr=proxy_host, port=proxy_port)
socket.socket = socks.socksocket

# Connect to the database via proxy
try:
    connection = psycopg2.connect(**conn_params)
    cursor = connection.cursor()

    # Example query
    query = sql.SQL("SELECT * FROM prospect;")
    cursor.execute(query)

    # Fetch results
    results = cursor.fetchall()
    print(results)

except Exception as e:
    print(f"Error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()

if __name__ == '__main__':
   app.run(debug=True)



