# -*- coding: utf-8 -*-
"""
HTTP Server
Respond to GET/POST requests

Validated on Python 2.7

Refer to: https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/


Here is a sample of basic http server using “BaseHTTPRequestHandler”. The example exposed two rest interfaces:
To ingest records into the web server
To retrieve already ingested records from the web server

Usage:
Copy paste the code above and name it simplewebserver.py
Starting WebServer:
python simplewebserver.py

POST add record example using curl:
curl -X POST http://localhost:8080/api/v1/addrecord/1 -d '{"id":100}' -H "Content-Type: application/json"

GET record example using curl:
curl -X GET http://localhost:8080/api/v1/getrecord/test     #does not exist this record
curl -X GET http://localhost:8080/api/v1/getrecord/1        #return info

"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import ujson as json
import urllib
import urlparse

class Recorder(object):
    def __init__(self):
        self.records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/api/v1/addrecord/*', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_data = json.loads(post_body)
                recordID = self.path.split('/')[-1]
                recorder.records[recordID] = json_data
                print "record %s is added successfully" % recordID
            elif ctype == 'application/x-www-form-urlencoded':
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_data = urlparse.parse_qs(post_body)    #decode for urllib.urlencode
                recordID = self.path.split('/')[-1]
                recorder.records[recordID] = json_data
                print "record %s is added successfully" % recordID
            else:
                data = {}
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_GET(self):
        if None != re.search('/api/v1/getrecord/*', self.path):
            recordID = self.path.split('/')[-1]
            if recorder.records.has_key(recordID):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(recorder.records[recordID])
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port):
        """

        Args:
            ip: 如果想让内网、外网、localhost等多个网址都能访问，可以设置成0.0.0.0
            port:
        """
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    '''
    #seems not necessary
    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord
    '''

    def stop(self):
        self.server.shutdown()
        self.waitForThread()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()

    recorder = Recorder()

    server = SimpleHttpServer(args.ip, args.port)
    print 'HTTP Server Running...........'
    server.start()
    server.waitForThread()
