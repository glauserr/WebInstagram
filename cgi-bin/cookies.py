#! /usr/bin/env python

import os
import datetime
import Cookie

def request_has_cookies():
    if os.environ.has_key('HTTP_COOKIE'):
        if os.environ['HTTP_COOKIE'] != "":
            return True
    return False


def get_session_cookie(session_id):

    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = session_id
    if os.environ.has_key("ASSIGNMENT1_SERVICE_HOST"):
        cookie["session"]["domain"] = "index-csci4140-projects.a3c1.starter-us-west-1.openshiftapps.com"
    else:
        cookie["session"]["domain"] = os.environ["REMOTE_HOST"]
    cookie["session"]["path"] = "/cgi-bin/"
    cookie["session"]["expires"] = \
        expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        
    # contains full html header. just send this #    
    return cookie.output()


def delete_session_cookie():
    cookie = Cookie.SimpleCookie()
    cookie['session']=''
    cookie['session']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

    return cookie.output()

def request_get_sessionID():
    session_id = -1
    strip = None
    if os.environ.has_key('HTTP_COOKIE'):
        for cookie in map(strip, os.environ['HTTP_COOKIE'].split( ';')):
            (key, value) = cookie.split('=')
            # user += value + " "
            # if key == "user":
            #     user = value

            if key == "session":
                session_id = value

    return session_id
    