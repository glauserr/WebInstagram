#! /usr/bin/env python

import cgi
import cgitb
import MySQLdb

from database import RegisterTable 

# cgitb.enable()

def register(form):

    pw1 = form.getvalue("pw1")
    pw2 = form.getvalue("pw2")
    user = form.getvalue("user")

    db_response = ""

    # if pw1 is not None and pw2 is not None and user is not None:
    if "pw1" in form and "pw2" in form and "user" in form:  
        if pw1 != pw2:
            db_response = "Passwords are not consistent"
            pass
        
        else:
            db = RegisterTable()
            
            if(db.is_registered(form["user"].value)):
                db_response = "Username not available. Try again"

            else:
                db_response = db.insert_query(("user", "pw"), (form["user"].value, form["pw1"].value))
                redirect ="""
                <html>
                <head>
                <title>A web page that points a browser to a different page after 2 seconds</title>
                <meta http-equiv="refresh" content="3"; /cgi-bin/index.cgi">
                <meta name="keywords" content="automatic redirection">
                </head>
                <body>
                    Registration successfull 
                </body>
                </html>
                """

    header = "Content-Type: text/html; charset=utf-8\n\n"

    html = """
        <div class="container">
        <form action="index.cgi" method="post">
            <b>Please insert:</b><br>
            <input type="hidden" name="action" value="register"></input>
            <input type="text" placeholder="Username" name="user" required><br>
            <input type="password" placeholder="Password" name="pw1" required><br>
            <input type="password" placeholder="Password again" name="pw2" required><br>

            <button type="submit">Sign up</button>
            <p> {}
            </p> 
        </form>
        </div>
        """.format(db_response,)

    # html output
    register_page = header + html

    if(db_response is True):
        print(redirect)    
    else:
        print(register_page)

