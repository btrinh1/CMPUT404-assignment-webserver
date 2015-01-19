import SocketServer
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Brian Trinh
# 
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

import os.path

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        path = os.path.join(os.getcwd(), "www") #www folder path joined to itempath
        line = self.data.splitlines()
        split = line[0].split() #['X', 'Y', 'Z'] format
        size = "0"
        ftype = " "
        output = ""

        if split[0] != "GET":
            response = "HTTP/1.1 404 Not Found\r\n"
            ctype = "Content-Type: text/html\r\n"
            output = "<html><body><b>Page not found.</b></body></html>\r\n"
        else:
            url = os.path.normpath(os.path.join(path +split[1]))           

            # If starts with our path and ends with '/''
            if (split[1].endswith("/") and url.startswith(path)):
                url = os.path.join(url, "index.html")

            # If .css or .html in our 'www' path
            #if(not os.path.isfile(url) and url.startswith(path))
            if (os.path.isdir(url) and url.startswith(path)):
                response = "HTTP/1.1 301 Moved Permanently\r\n"
                ctype = "Content-Type: text/html\r\n"
                ftype = "redir"
            elif (os.path.isfile(url) and url.startswith(path)):
                response = "HTTP/1.1 200 OK\r\n"

                if url.endswith(".html"):
                    ftype = "html"
                    ctype = "Content-Type: text/html\r\n"
                elif url.endswith(".css"):
                    ftype = "css"
                    ctype = "Content-Type: text/css\r\n"

                file = open(url)
                output = file.read()
                file.close()
            # 404 for when /www/do-not-implement-this-page-it-is-not-found etc
            else:
                response = "HTTP/1.1 404 Not Found\r\n"
                ctype = "Content-Type: text/html\r\n"
                output = "<html><body><b>Page not found.</b></body></html>\r\n"
                                    
        # Content-length logic / redirect
        if(ftype == "html" or ftype == "css"):
            clength = str(os.path.getsize(url)) + "\r\n\r\n"  
        # If is 3XX redirect then instead of content-length specify location of redirect
        elif(ftype == "redir"):
            clength = "Location: %s/\r\n\r\n" %(split[1])
        else:
            clength = "\r\n\r\n"
        
        # Construct the final output
        self.request.sendall(response
                             + ctype 
                             + clength 
                             + output)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
