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
              "http"  : 'fixie:k2KJ04rPQQ047n8@speedway.usefixie.com:1080',
              "https" : 'fixie:k2KJ04rPQQ047n8@speedway.usefixie.com:1080'
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
    database_url = "postgres://ucrol25emqd2ch:p31d791a3fe8bcb5b5102d7b8b43f08ca70ee2cc9d7943c23b4db6b110324346e@ec2-52-2-248-148.compute-1.amazonaws.com:5432/d2r45oj3jf7gs7"
    url = urlparse(database_url)
    print(f"url: {url}")
    # Set up SOCKS proxy
    socks_host = "fixie:k2KJ04rPQQ047n8@speedway.usefixie.com:1080"
    socks_port = 1080  # Change to the actual port used by your SOCKS proxy
    
    socks_proxy = socks.socksocket()
    socks_proxy.setproxy(socks.PROXY_TYPE_SOCKS5, socks_host, socks_port)
    
    # Connect to PostgreSQL
    try:
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            connection_factory=socks_proxy
        )
    
        # Create a cursor
        cursor = connection.cursor()
    
        # Execute your SQL queries here
    
        # Commit changes
        connection.commit()
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()

@app.route('/new')
def newRoute():
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, proxy.hostname, 1080, True, proxy.username,proxy.password)
    host = "httpbin.org"
    print('host: ',s)
    s.connect((host))
    print('s: ',s)

    request = "GET /ip HTTP/1.1\nHost: "+host+"\nUser-Agent:Mozilla 5.0\n\n"
    s.send(request)

    response = s.recv(1024)
    # print response.text

if __name__ == '__main__':
   app.run(debug=True)
