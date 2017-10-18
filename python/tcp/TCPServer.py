# -*- coding: utf-8 -*-
"""
TCP Server

Validated in Python 2.7
"""

import SocketServer
from time import ctime
HOST = ''
PORT = 21567
ADDR = (HOST, PORT)
class MyRequestHandler(SocketServer.BaseRequestHandler):
   def handle(self):
       print '...connected from:', self.client_address
       while True:
           self.request.sendall('[%s] %s' % (ctime(),self.request.recv(1024)))
tcpServ = SocketServer.ThreadingTCPServer(ADDR, MyRequestHandler)
print 'waiting for connection...'
tcpServ.serve_forever()

