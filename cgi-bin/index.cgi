#! /usr/bin/env python

import os
import sys
# import Cookie
# import login
import cgi
import cgitb
import cookies
import util
from database import SessionTable
from database import ImageTable
from database import AdminTable
from action_login import login
from action_logout import logout
from action_register import register
from action_update import update
from action_upload import upload

# cgitb.enable()


user = None
display_public = False
loggedIn = False
err = None
session_id = 0
page = 1
num_pages = 1
next_disabled = "disabled"
back_disabled = "disabled"
img_per_page = 8
action = None


try:
    # check system
    if not AdminTable().exists():
        print("""Content-type: text/html; charset=utf-8\n\n
            <!DOCTYPE html>
            <html lang="en"><head></head> 
            <body>
            <h1>System is not initialized</h1>
            <p>Setup system via initialization page </p>
            </body>
            </html>
            """)
        sys.exit()
        pass

    form = cgi.FieldStorage()

    if "action" in form:
        action = form.getvalue("action")

    # perform routing (Openshift does not support multi routing...!!!)
    if action == "login":
        login(form)
        sys.exit()
        pass

    if action == "logout":
        logout(form)
        sys.exit()
        pass

    if action == "register":
        register(form)
        sys.exit()
        pass

    if action == "update":
        update(form)
        sys.exit()
        pass

    if action == "upload":
        upload(form)
        sys.exit()
        pass

    if cookies.request_has_cookies():
        session_id = cookies.request_get_sessionID()

        # TODO: check cookie still valid
        st = SessionTable()
        if st.sid_is_used(session_id):
            loggedIn = True
            user = st.get_user(session_id)
            # private
            display_public = False
            checked_str = "checked"
        else:
            pass

    # per default show public
    if "public" in form and form.getvalue("public"):
        # set private
        display_public = False
        checked_str = "checked"

    else:  # set public
        display_public = True
        checked_str = ""

    # paging
    if "p_back" in form:
        page = int(form.getvalue("p_back"))

    elif "p_next" in form:
        page = int(form.getvalue("p_next"))
    else:
        pass

    it = ImageTable()
    if loggedIn:
        img_paths = it.get_image_list(user, None, None)

    else:  # not logged in
        img_paths = it.get_image_list(None, True, None)

    # page update
    num_pages = (len(img_paths) + img_per_page - 1) / img_per_page
    if num_pages == 0:
        num_pages = 1

    if page > 1:
        back_disabled = ""  # not disabled

    if page < num_pages:
        next_disabled = ""  # not disabled

    # creat html
    header = "Content-Type: text/html; charset=utf-8\n\n"

    html_head = """
        <!DOCTYPE html>
        <html lang="en">      
        <head>
          <p style="font-size:32px">Webinstagram</p>
        </head>"""

    html_body = """
        <body>"""

    if loggedIn:
        html_body += """
              <p>
                Hello {}
              </p>""".format(user)

    # apply paging
    pos = (page - 1) * img_per_page
    page_end = pos + img_per_page

    if page_end > len(img_paths):
        page_end = pos + (len(img_paths) % img_per_page)

    host = ""
    if os.environ.has_key("ASSIGNMENT1_SERVICE_HOST"):
        host = "http://root-csci4140-projects.a3c1.starter-us-west-1.openshiftapps.com"
    
    while pos < page_end:
        if pos % 4 == 0:
            html_body += "<br>"

        html_body += """
          <img src="{}{}" alt="HTML5 Icon" style="height: 100%; width: 100%; max-width: 200px; max-height: 200px">
          """.format(host, img_paths[pos])
        pos += 1

    html_body += """
          <div class="container">
            <form action="index.cgi" method="post">
              <p>
              <button type="submit" name="p_back" value="{}" {}>Back</button>
              Page: {} of {}
              <button type="submit" name="p_next" value="{}" {}>Next</button>
              </p>    
            </form> 
          </div>
          """.format(page - 1, back_disabled,
                     page, num_pages, page + 1, next_disabled)

    if loggedIn:
        html_body += """
              <div class="container">
                <form action="index.cgi" method="post">
                  <input type="hidden" name="action" value="logout"></input>
                  <button type="submit">Logout</button>
                </form>
              </div>
              <div class="container">
                <form action="index.cgi" method="post">
                  <input type="hidden" name="action" value="update"></input>
                  <button type="submit">Change Password</button>
                </form>
              </div>
              <br>
              <form enctype="multipart/form-data" action="index.cgi" method="post">
                <input type="hidden" name="action" value="upload"></input>
                <input type="file" name="filename">
                <input type="hidden" name="userID" value="{}"></input>
                <label for="cb">public</label>  
                <input type="checkbox" id="cb" name="public" value="True">
                <button type="submit">Upload</button>     
              </form>
            """.format(user,)

    else:
        html_body += """
                <form method="post" action="index.cgi">
                  <input type="hidden" name="action" value="login"></input>
                  <button type="submit">Login</button>
                </form>
                <form method="post">
                  <input type="hidden" name="action" value="register"></input>
                  <button type="submit" formaction="index.cgi">Sign up</button>
                </form>
              <div class="container">
              </div>
              <div class="container">
              <div>
              """

    html_body += """
        </body>
        </html>"""

    print(header + html_head + html_body)
    pass

except SystemExit as ex:
    pass
