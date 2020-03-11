'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

    This task is designed by Praveen Garimella and is to be used
    as part of the Learning by Doing, Project Based Course on Operating Systems
    Write to pg@fju.us for any questions or comments
'''

'''
    == Task 2 ==
    This file has the solution for M1 and the description for M2.
    Review this solution before you start implementing the M2.
    If you don't like our solution for M1 then
    tell us why so that we can improve it.

    In the M2 you have to write code to handle http requests for static content.
    Web servers maintain static content in a directory called document root.
    We have provided you with a directory with the name www.
    This directory has some html files and images.
    A web server may receive a request to access one of these files.

    When such a request is received you have to parse the HTTP request
    and extract the name of the file in the request aka Uniform Resourse Indicator    
    Learn the format of the http requests from the tutorial given below.
    https://www.tutorialspoint.com/http/http_requests.htm

    After extracting the URI,
    check if the file exists in the document root directory i.e., www

    If it exists, you have to read the file contents as the response data.
    If not you have to send a 404 file not found response.

    Construct the http response by invoking response_headers method
    This method is provided in the HTTPServer class
    Passing the appropriate response code, content type and length to the method
    
    A tricky part to the response construction is to identify the content type.
    Set the content type text/html for files that end with the extension .html
    
    What would be the content type for images? Review the link below.
    https://www.iana.org/assignments/media-types/media-types.xhtml#image

    How do we figure out the content subtype of an image?
    Explore the use of the library mimetype in python.
    https://www.tutorialspoint.com/How-to-find-the-mime-type-of-a-file-in-Python
'''

import socket
import os, sys
import mimetypes, time, signal
path = "/home/dharshak/Desktop/MSIT/IOS-Python/tws-m5"

class HTTPServer:
    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.s.bind((IP, port))
            self.s.listen()
            while True:
                conn, addr = self.s.accept()
                with conn:
                    print('Connected by', addr)
                    # TODO read the request and extract the URI
                    uri = str(conn.recv(1024).decode()).split(" ")[1]
                    # TODO update the parameter with the request URI
                    # uri = msg_split[1]
                    code, c_type, c_length, data = self.get_data(uri)
                    response = self.response_headers(code, c_type, c_length) + data
                    conn.sendall(bytes(response))
                    conn.close()
    
    def get_data(self, uri):
        '''
            TODO: This function has to be updated for M2
        '''
        if(uri=="/"):
            uri = path + uri
            data = ""
            for i in os.listdir(uri):
                data = data + '<a href=\"' + i + '\">' + i + '</a><br>'
            return 200, "text/html", len(data), data.encode()
        else:
            data = ""
            if(os.path.isdir(path + uri)):
                for i in os.listdir(path + uri):
                    data = data + '<a href=\"' + uri + "\\" + i + '\">' + i + '</a><br>'
                return 200, "text/html", len(data), data.encode()
            elif(os.path.isfile(path + uri)):
                output = mimetypes.MimeTypes().guess_type(path + uri)[0]
                if "bin" in uri:
                    stdin = sys.stdin.fileno()
                    stdout = sys.stdout.fileno()
                    childIn,parentOut = os.pipe()
                    parentIn,childOut = os.pipe()
                    pid = os.fork()
                    st = ""
                    if pid == 0:
                        os.close(parentOut)
                        os.close(parentIn)
                        os.dup2(childOut,stdout)
                        # if "bin/ls" in uri:
                        #     args=[path+uri]
                        #     os.execvp(args[0], args)
                        # elif "bin/du" in uri:
                        #     args=[path+uri]
                        #     os.execvp(args[0], args)
                        # el
                        if "forever" in uri:
                            args=["sh",path+uri]
                            os.execvp(args[0],args)
                        else:
                            exec(open(path+uri).read())
                            os._exit(0)
                    else:
                        os.close(childOut)
                        os.close(childIn)
                        os.dup2(parentIn,stdin)
                        time.sleep(3)
                        p,status = os.waitpid(pid, os.WNOHANG)
                        print(p)
                        print(status)
                        if p == 0:
                            os.kill(pid, signal.SIGSTOP)
                            data = "<h1> Timeout : Process terminated </h1>"
                            return 200, "text/html", len(data), data.encode()
                        else:
                            stdin = os.fdopen(parentIn,'r')
                            for i in stdin:
                                st += i
                            return 200, "text/html", len(st), st.encode()
            else:
                try:
                    data = open(path + uri,'rb').read()
                    return 200, output, len(data), data
                except:
                    data = "<h1>File Not Found</h1>"
                    return 404, "text/html", len(data), data.encode()
    def response_headers(self, status_code, content_type, length):        
        # TODO update this dictionary for 404 status codes
        response_code = {200: "200 OK",404: "404 File Not Found"}
        headers = ""
        headers += "HTTP/1.1 " + response_code[status_code] + "\n"
        headers += "Content-Type: " + content_type + "\n"
        headers += "Content-Length: " + str(length) + "\n"
        headers += "Connection: close" + "\n"
        headers += "\n"
        return headers.encode()

def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

if __name__ == "__main__":
    main()                   