#  coding: utf-8
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2019 Irene Gao
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):


    def handle(self):
        self.data = str(self.request.recv(1024).strip(),'utf-8')
        #print ("Got a request of: %s\n" % self.data)
        # initialize

        method = self.data.split()[0]
        url = self.data.split()[1]
        cur_path = os.path.dirname(os.path.abspath(__file__)) + "/www"
        abs_path = cur_path + url
        resp = " "
        print(url)
        if method == 'GET':
            if os.path.isfile(abs_path):
                if '.html' in abs_path:
                    openfile = open(abs_path).read()
                    resp = "HTTP/1.1 200 OK contents of \n" + "Content-Type: text/html\n" + "\n"
                    final = resp + openfile
                elif '.css' in abs_path:
                    openfile = open(abs_path).read()
                    resp = "HTTP/1.1 200 OK contents of \n" + "Content-Type: text/css\n" + "\n"
                    final = resp + openfile
                else:
                    resp = "HTTP/1.1 404 Not Found\n" + "Content-Type: text/plain\n" + "\n"
                    final = resp
            elif os.path.isdir(abs_path):
                if os.path.isfile(abs_path+ "index.html"):
                    openfile =  open(abs_path + "index.html").read()
                    resp = "HTTP/1.1 200 OK contents of \n" + "Content-Type: text/html\n" + "\n"
                    final = resp + openfile
                elif url[-1:] == "/":
                    openfile = open(abs_path).read()
                    resp = "HTTP/1.1 200 OK contents of \n" + "Content-Type: text/html\n" + "\n"
                    final = resp + openfile
                elif url[-1:] != "/":
                    resp = "HTTP/1.1 301 Permanently moved to \n" + "Content-Type: text/html\n" + "\n"
                    final = resp
                else:
                    resp = "HTTP/1.1 404 Not Found\n" + "Content-Type: text/plain\n" + "\n"
                    final = resp
            else:
                resp = "HTTP/1.1 404 Not Found\n" + "Content-Type: text/plain\n" + "\n"
                final = resp
        else:
            resp = "HTTP/1.1 405 Method Not Allowed\n" + "Content-Type: text/plain\n" + "\n"
            final = resp

        print(final)
        self.request.sendall(bytearray(final,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
