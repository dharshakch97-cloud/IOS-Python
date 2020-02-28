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
import os,mimetypes
root = "/home/dharshak/Desktop/MSIT/IOS-Python/tws-m2"
enable_directory_browser = True

def get_files(path):
    files = []
    for file in os.listdir(root + path):
        if(path == root):
            files.append("<a href = \""+file + "\" > " + file + "</a> <br>")
        else:
            files.append("<a href = \""+os.path.join(path,file) + "\" >" + file + "</a> <br>")
    return ''.join(files)    
def get_content_type(path):
    typ, a = mimetypes.guess_type(root + path)
    if typ is None:
        return "text"
    else:
        return typ    

def init(IP, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((IP, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                # TODO read the request and extract the URI
                input = conn.recv(1024).decode("UTF-8")
                uri = input.split(" ")[1]
                flag = os.path.exists(root + uri)
                if input.split(" ")[0] != 'GET' or uri ==" ":
                    response = b'''\
HTTP/1.1 404 File Not Found
Content - Type:html

<h1>bad request </h1>'''
                elif flag == False:
                    response = b"""\
HTTP/1.1 404 File Not Found
Content - Type:html

<h1>File Not Found<h1>""" 
                elif enable_directory_browser:
                    if uri == "/favicon.ico":
                        pass
                    elif flag and os.path.isfile(root + uri):
                        content_type = get_content_type(uri)
                        f = open(root + uri, 'rb')
                        string = f.read()
                        response = b"""\
HTTP/1.1 200 OK
Content - Type: """ +bytes(content_type,"UTF-8")+b"""l

""" + string
                    else:
                        response = b"""\
HTTP/1.1 200 OK
Content - Type:html

""" + bytes(get_files(uri), "UTF-8")

                else:
                    response = b"""\
HTTP/1.1 400 BAD REQUEST
Content-Type: html;

<h1>BAD REQUEST</h1>"""                             
                
                conn.sendall(response) 
                conn.close()

def main():
# test harness checks for your web server on the localhost and on port 8888
# do not change the host and port
# you can change  the HTTPServer object if you are not following OOP
    init('127.0.0.1', 10000)

if __name__ == "__main__":
    main()



