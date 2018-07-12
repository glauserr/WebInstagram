=============================
Webinstagram 
=============================

------------
Introduction
------------
Create your own online public or private photo collection.

The application provides the following functionalities:

- online photo album
- create account
- update password
- login to your personal space to upload photos
- upload public and private photos
- 5 image filters 


Administrator:

- system initialization and re-initialization 

http://index-csci4140-projects.a3c1.starter-us-west-1.openshiftapps.com/cgi-bin/index.cgi


---------------
Initialization
---------------
The system can be initialized and re-initialized via a separate link with the following login data: 

- Admin username: admin
- Admin password: webinstagram2018

http://initialization-csci4140-projects.a3c1.starter-us-west-1.openshiftapps.com/cgi-bin/init.cgi


-------------------------
Setup system on openshift
-------------------------
ImageMgick and MySQL database on openshift

ImageMgick is required: 

1. connect to pod 

oc rsh <pod>

2. get package:

wget https://www.imagemagick.org/download/ImageMagick.tar.gz

3. extract

tar xvf ImageMagick.tar.gz

4. go in folder and run configuration

./configure --prefix=/opt/app-root

5. compile

make

6. installation

make install  


MySQL database has to be set up on openshift:

1. Choose MySQL (Persistent) on openshift and follow the steps

2. Connect application to database

oc env dc phpdatabase -e MYSQL_USER=myuser  -e MYSQL_PASSWORD=mypassword -e MYSQL_DATABASE=mydatabase


--------
Database
--------
A MySQL database is used (MySQLdb lib). It is located on openshift in a separate pod. The application connects to the database and stores 4 tables:

- Administrator table: 	admin infos e.g. name, password
- User table: 			usernames, passwords and creation time. 
- Session table:		stores session id per login
- Image table:			stores link to image files including upload username and upload date

Request for bonus

- Please consider the work to set up a remote database connection to the application including the well-coded database interface in cgi-bin/database.py  


-------------------
System Organization
-------------------
The Application is basecly structured with 4 folders:

- cgi-bin:		consits of all cgi-files (index.cgi and init.cgi) and python files
				- action_*.py are used for specific functionalities (login, upload etc)
				- *.py provides gerneral classes or functions to the application 

- img: 			folder to store uploaded images
- tmp:			temporary storage while uploading process (for filters) 
- util:			general resources

And app.py as system entry point. 


-----
Notes 
-----
Setup system on local machine:

There, the database is running remotely on openshift as a pod, we have to connect to them.

1. run configure.sh. It will start forwarding localhost request to openshift mysql
2. read out form shell IP (e.g 127.0.0.1) 
3. set IP in cgi-bin/database.py (variable server = IP)
4. And set correct login data to your database (name, password, dbname)

Note: requires oc 	



Bugs and not fully completed:

Unfortunately, the first initialization process always terminates with a loose in connection on OPENSHIFT (not on local machine). I was not able to figure out why this occures. 

- Error message: 
Exception happened during processing of request from ('10.130.2.1', 43452)
Traceback (most recent call last):
  File "/opt/rh/python27/root/usr/lib64/python2.7/SocketServer.py", line 290, in _handle_request_noblock
    self.process_request(request, client_address)
  File "/opt/rh/python27/root/usr/lib64/python2.7/SocketServer.py", line 318, in process_request
    self.finish_request(request, client_address)
  File "/opt/rh/python27/root/usr/lib64/python2.7/SocketServer.py", line 331, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "/opt/rh/python27/root/usr/lib64/python2.7/SocketServer.py", line 652, in __init__
    self.handle()
  File "/opt/rh/python27/root/usr/lib64/python2.7/BaseHTTPServer.py", line 340, in handle
    self.handle_one_request()
  File "/opt/rh/python27/root/usr/lib64/python2.7/BaseHTTPServer.py", line 328, in handle_one_request
    method()
  File "/opt/rh/python27/root/usr/lib64/python2.7/SimpleHTTPServer.py", line 45, in do_GET
    f = self.send_head()
  File "/opt/rh/python27/root/usr/lib64/python2.7/CGIHTTPServer.py", line 69, in send_head
    return self.run_cgi()
  File "/opt/rh/python27/root/usr/lib64/python2.7/CGIHTTPServer.py", line 235, in run_cgi
    if not self.rfile.read(1):
  File "/opt/rh/python27/root/usr/lib64/python2.7/socket.py", line 384, in read
    data = self._sock.recv(left)
error: [Errno 104] Connection reset by peer


Therefore, Request for Password change is missing. 


