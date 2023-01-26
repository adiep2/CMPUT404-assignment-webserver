#  coding: utf-8 
import socketserver
import mimetypes
from os import path, getcwd

# Copyright 2022 Abram Hindle, Eddie Antonio Santos, Aaron Diep
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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        requestArray = self.data.split()
        if requestArray[0].decode("utf-8") == "GET":
            requestPath = requestArray[1].decode("utf-8")
            redirect = False
            if requestPath[len(requestPath) - 1] == '/':
                requestPath = requestPath + "index.html"
            elif "." not in requestPath and path.isdir("www" + requestPath):
                self.request.sendall(bytearray("HTTP/1.0 301\n", "utf-8"))
                location = "Location: " + requestPath + "/\r\n"
                self.request.sendall(bytearray(location, "utf-8"))
                redirect = True
            if not redirect:
                fileType = mimetypes.guess_type(requestPath)
                filePath = "www" + requestPath
                scriptPath = getcwd() + "/www"
                absPath = path.abspath(filePath)
                if (path.exists(filePath) and scriptPath in absPath):
                    report_file = open(filePath)
                    file = report_file.read()
                    self.request.sendall(bytearray("HTTP/1.0 200 OK\r\n", "utf-8"))
                    if fileType[0] is not None:
                        contentType = "Content-Type: " + fileType[0] + "\r\n"
                        self.request.sendall(bytearray(contentType, "utf-8"))
                    self.request.sendall(bytearray("\r\n", "utf-8"))
                    self.request.sendall(bytearray(file, "utf-8"))
                else:
                    self.request.sendall(bytearray("HTTP/1.0 404\n", "utf-8"))
        else:
            self.request.sendall(bytearray("HTTP/1.0 405\n", "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
