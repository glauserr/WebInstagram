#! /usr/bin/env python

import os, sys, cgi, cgitb
import database
import util

# cgitb.enable()

_image_dir = "img/"
_tmp_dir = "tmp/"

def show_pw_change(info=""):
    html = """"Content-Type: text/html; charset=utf-8\n\n
        <!DOCTYPE html>
        <html lang="en">      
        <head>
          <p style="font-size:32px">First initialization</p>
        </head>
        <body>  
        <form action="init.cgi" method="post">
          <div class="container">
            <b>Please change password:</b><br><br>
            <input type="hidden" name="init" value="pw_change"></input>
            <input type="password" placeholder="password" name="pw1" required><br>
            <input type="password" placeholder="re-type password" name="pw2" required><br><br>
            <button type="submit">Apply</button>
          </div>
        </form>
        <p>{}</p>
        </body>
        </html>""".format(info)
    return html


def delete_imgs(img_direcotry):
    retVal = True

    it = database.ImageTable()

    for the_file in os.listdir(img_direcotry):
        file_path = os.path.join(img_direcotry, the_file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                it.delete_image("/" + _image_dir + the_file)

            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            # print(e)
            retVal = False

    return retVal


def sys_re_initialization():
    retVal = delete_imgs(os.path.abspath(_image_dir))
    try:
        st = database.SessionTable()
        rt = database.RegisterTable()

        if st.exists():
            st.delete_all()
        else:
            st.create()

        if rt.exists():
            rt.delete_all()
        else:
            rt.create()
    except:
        retVal = False

    return retVal


def sys_initialization():
    retVal = True
    try:
        st = database.SessionTable()
        rt = database.RegisterTable()
        it = database.ImageTable()
        at = database.AdminTable()

        if st.exists():
            st.drop()

        if rt.exists():
            rt.drop()

        if it.exists():
            it.drop()

        if at.exists():
            at.drop()

        st.create()
        rt.create()
        it.create()
        at.create()

        # img_path = os.path.abspath(_image_dir)
        # if not os.path.exists(img_path):
        #     os.mkdir(img_path)

        # tmp_path = os.path.abspath(_tmp_dir)
        # if not os.path.exists(tmp_path):
        #     os.mkdir(tmp_path)

        it.insert(("admin", "/util/world.jpeg"), True)

    except:
        retVal = False
    # run configuration script 
    # os.system("./configure.sh")
    return retVal

_default_admin = "admin"
_default_pw = "webinstagram2018"
_init = None

try:
    form = cgi.FieldStorage()

    if "init" in form:
        _init = form.getvalue("init")

    try: 
        if _init == "login":

            message = ""

            if "admin" in form and "pw" in form:
                _admin = form.getvalue("admin")
                _pw = form.getvalue("pw")

                # first initialization
                at = database.AdminTable()
                if at.exists():
                    # os.system("echo first > re_init.txt" )

                    if at.is_registered(_admin) and at.get_pw(_admin) == _pw:
                        if sys_re_initialization():
                            print(util.html_redirect("init.cgi", 1000, "<h1>Re-initialization Successfull!</h1><p>Webinstagram now ready</p>"))
                            pass
                        else:
                            print(util.html_redirect_with_button("init.cgi", "try again", 20,"Re-initialization Failed"))
                            pass
                        os.system("echo first > re_init_done.txt")
                        sys.exit()

                    else:
                        message = "Invalid admin name or password. Please try again"
                    pass

                else:
                    # PW change not working on openshift
                    # output = show_pw_change()
                    # print(output)
                    if sys_initialization():
                        print(util.html_redirect("init.cgi", 1000, "<h1>Initialization Successfull!</h1><p>Webinstagram now ready</p>"))
                        at = database.AdminTable()
                        at.insert(("admin", _pw, "True"))
                    else:
                        print(util.html_redirect_with_button("init.cgi", "try again", 20, "Initialization Failed"))

                    sys.exit()

            html = """Content-Type: text/html; charset=utf-8\n\n
            <!DOCTYPE html>
            <html lang="en">      
            <head>
              <p style="font-size:32px">Login System Initialization</p>
            </head>
            <body>  
                <form action="/cgi-bin/init.cgi" method="post">
                  <div class="container">
                    <input type="hidden" name="init" value="login"></input>
                    <input type="text" placeholder="Enter Admin" name="admin" required>
                    <input type="password" placeholder="Enter Password" name="pw" required>
                    <button type="submit">Login</button>
                    <label><b>{}</b></label>
                  </div>
                </form>
            </body>
            </html>""".format(message,)
            print(html)
            sys.exit()


        if _init == "pw_change":
            if "pw1" in form and "pw2" in form:

                # os.system("echo first > pw_change.txt")
                if sys_initialization():

                    new_pw = form.getvalue("pw1")
                    if new_pw == _default_pw:
                        output = show_pw_change("Password not valid choose another one")
                        print(output)
                        sys.exit()

                    at = database.AdminTable()
                    at.insert(("admin", new_pw, "True"))

                    print(util.html_redirect("init.cgi", 1000, "<h1>Initialization Successfull!</h1><p>Webinstagram now ready</p>"))
                    sys.exit()

                print(util.html_redirect_with_button("init.cgi", "try again", 20, "Initialization Failed"))
                # os.system("echo first > pw_change_done.txt")
                sys.exit()

        # default first page
        html = """Content-Type: text/html; charset=utf-8\n\n
            <!DOCTYPE html>
            <html lang="en">      
            <head>
              <p style="font-size:32px">System Initialization</p>
            </head>
            <body>
              <p> Important: All data will be deleted </p>
              <div class="container">
                <form method="post">
                  <button type="submit" name="init" value="login" formaction="init.cgi">Initialize</button>
                </form>
              </div>
            </body>
            </html>"""
        print(html)

        #exit 
    except SystemExit as ex:
        # os.system("echo first > exit.txt" )
        pass

except Exception as err:
    os.system("echo %s > error_log.txt" % err)
    pass