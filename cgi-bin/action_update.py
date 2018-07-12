#! /usr/bin/env python

import cgi, sys
import cgitb
import util, cookies

from database import RegisterTable
from database import SessionTable

# cgitb.enable()

def update(form):
    try:

        db_response = ""

        if "pw1" in form and "pw2" in form and "pw_old" in form:

            if form["pw1"].value != form["pw2"].value:
                db_response = "Passwords are not consistent"    
                pass
            
            else:

                st = SessionTable()
                db = RegisterTable()

                user = st.get_user(cookies.request_get_sessionID())

                if(db.get_pw(user) != form["pw_old"].value):
                    db_response = "Invalid password. Try again"

                else:
                    if db.change_pw(user, form["pw1"].value):
                        print(util.html_redirect("index.cgi", 3, "<p> change successfull </p>"))
                        sys.exit()
                    else:
                        db_response = "Invalid password. Try again"
                    # redirect="""
                    #     <form action="index.cgi" method="post">
                    #       <div class="container">
                    #         <button type="submit">Login</button>    
                    #       </div>
                    #     </form>
                    #     """


        header = "Content-Type: text/html; charset=utf-8\n\n"

        html = """
            <form action="index.cgi" method="post">
              <div class="container">
                <b>Please insert:</b><br>
                <input type="hidden" name="action" value="update"></input>
                <input type="password" placeholder="current password" name="pw_old" required><br>
                <input type="password" placeholder="password" name="pw1" required><br>
                <input type="password" placeholder="retype password" name="pw2" required><br>

                <button type="submit">Update</button>
              </div>
            </form>
            <p> {} </p>
            """.format(db_response)

        # html output
        print(header)
        print(html)

    except SystemExit as ex:
        pass