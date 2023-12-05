import os, requests
from flask import Flask

import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
import socks
import socket
# from urlparse import urlparse

app = Flask(__name__)

proxyDict = {
              "http"  : 'https://r09cndoizux678:44m6nmtadw9bg10eowfxi45cyrbyku@us-east-shield-04.quotaguard.com:9294',
              "https" : 'https://r09cndoizux678:44m6nmtadw9bg10eowfxi45cyrbyku@us-east-shield-04.quotaguard.com:9294'
 }

 # Extract proxy connection details from env variable
proxy = urlparse('https://r09cndoizux678:44m6nmtadw9bg10eowfxi45cyrbyku@us-east-shield-04.quotaguard.com:9294')

@app.route('/')
def hello():
    # return 'Hello from Python!'
    r = requests.get('https://www.google.com', proxies=proxyDict)
    # r = requests.get('https://www.google.com')
    return r.text

def get_public_ip():
    try:
        # Use a service that echoes the client's IP address
        response = requests.get('https://api64.ipify.org?format=json')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response and extract the IP address
            ip_address = response.json()['ip']
            return ip_address
        else:
            print(f"Error: Unable to fetch IP address. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    # Get and print the public IP address
    my_ip = get_public_ip()
    print(f"My public IP address is: {my_ip}")

@app.route('/dbconnect')
def connect():
    my_ip = get_public_ip()
    print(f"My public IP address is: {my_ip}")
    # Parse the database URL
    db_url = "postgres://ucrol25emqd2ch:p31d791a3fe8bcb5b5102d7b8b43f08ca70ee2cc9d7943c23b4db6b110324346e@ec2-52-2-248-148.compute-1.amazonaws.com:5432/d2r45oj3jf7gs7"
    url = urlparse(db_url)
    # Set up the proxy settings
    print(proxyDict)
    proxy_host = proxyDict['http']
    # proxy_ips = ['54.173.229.200', '54.175.230.252']
    proxy_ips = ['54.160.232.145', '44.215.229.88']
    proxy_port = 1080
    proxy_type = socks.SOCKS5  # Change this based on your proxy type

    selected_proxy_ip = proxy_ips[0]
    # Set up the connection parameters
    conn_params = {
        'database': url.path[1:],
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
        'sslmode': 'require',  # Use 'require' to enable SSL
        'sslcert': '/postgresql.crt',  # Path to client certificate file
        'sslkey': '/postgresql.key'  # Pat
    }

    # Set up the proxy
    socks.set_default_proxy(proxy_type, addr=proxy_host)
    socket.socket = socks.socksocket

    # Connect to the database via proxy
    try:
        connection = psycopg2.connect(**conn_params)
        cursor = connection.cursor()

        # Example query
        query = sql.SQL('SELECT * FROM pgadmin."Prospect" limit 1;')
        cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()
        print('results:', results)
        return "private_working"

    except Exception as e:
        print(f"Error: {e}")

    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()

@app.route('/new')
def newRoute():
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, proxy.hostname, 1080, True, proxy.username,proxy.password)
    host = "httpbin.org"
    s.connect((host, 80))
    print('s: ',s)

    request = "GET /ip HTTP/1.1\nHost: "+host+"\nUser-Agent:Mozilla 5.0\n\n"
    s.send(request)

    response = s.recv(1024)
    # print response.text

if __name__ == '__main__':
   app.run(debug=True)
