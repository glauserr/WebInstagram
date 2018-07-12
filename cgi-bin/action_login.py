#! /usr/bin/env python

import os, sys
import cgi, cgitb
import datetime
import random
import database
import cookies, util

import Cookie

cgitb.enable()

def login(form):
    pw = str()
    user = str()
    error = str()
    message = str()
    login_success = False

    if "user" in form and "pw" in form:

        user = form.getvalue("user")
        pw = form.getvalue("pw")

        try:
            db = database.RegisterTable()
            st = database.SessionTable()
            session_id = None

            if db.is_registered(user) and db.get_pw(user) == pw:

                sid_used = True
                while(sid_used):
                    session_id = random.randint(10000000, 99999999)
                    sid_used = st.sid_is_used(session_id)

                if st.insert((user, session_id)):

                    # cookies not working on openshift!! 
                    header = cookies.get_session_cookie(session_id)
                    header += header

                    redirect = util.html_redirect("index.cgi")

                    html = redirect

                    login_success = True

                else:
                    error = "500 Internal Server Error"

            else:
                message = "Invalid username or password"

        except Exception as err:        
            error = "500 Internal Server Error"

    if not login_success:
        header = "Content-Type: text/html; charset=utf-8\n\n"
        html = """
        <p style="font-size:32px">Login</p>
        <div class="container">
        <form action="/cgi-bin/index.cgi" method="post">
            <input type="hidden" name="action" value="login"></input>
            <label for="user"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="user" required>

            <label for="pw"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" name="pw" required>
            <button type="submit">Login</button>
            <label><b>{}</b></label>
        </form>
        </div>
        """.format(message,)

    if error:
        header = "Content-Type: text/html; charset=utf-8\n\n"
        html = """<html><head>{}</head></html>""".format(error,)

    # html output
    print(header)
    print(html)

