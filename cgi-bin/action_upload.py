#!/usr/bin/env python

import cgi
import cgitb
import os
import sys
import datetime
# import PythonMagick as Magick
from PIL import Image
# import PIL
from database import ImageTable
import filters
import util

# cgitb.enable()

# try:  # Windows needs stdio set for binary mode.
#     import msvcrt
#     msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
#     msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
# except ImportError:
#     pass


def upload(form):
    message = None


    # temporary data storage
    tmp_img_dir = os.path.abspath("") + "/tmp/"
    history = None
    h_lines = list()
    write_history = True

    # image infos
    ispublic = None
    img_type = str()
    img_width = str()
    img_height = str()


    # upload file to tmp
    if "filename" in form:
        fileitem = form["filename"]

        # check if public img
        if "public" in form:
            ispublic = True
        else:
            ispublic = False

        # temporary, store file
        test_img_path = tmp_img_dir + datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S-%f")
        open(test_img_path, 'wb').write(fileitem.file.read())

        try:
            img = Image.open(test_img_path)
            img_width, img_height = img.size
            img_type = img.format.lower()

            img_type = img_type.replace("jpeg", "jpg")

            # create extension aware path
            tmp_img_path = test_img_path + "." + img_type
            img.save(tmp_img_path)

        except Exception as err:
            os.remove(test_img_path)
            html_body = """<p>Invalid image file (no jpg, png or gif) </p>
                           <p>Returning to index page...</p>
                        """
            print(util.html_redirect("index.cgi", 3, html_body))
            sys.exit()

        os.remove(test_img_path)

    # userID should always be re-transmitted
    if "userID" in form:
        user = form.getvalue("userID")

        # get history data
        history = os.path.join(os.path.dirname(__file__),
                               tmp_img_dir + user + ".txt")
        if os.path.isfile(history):
            hf = open(history, 'r')
            h_lines = hf.read().splitlines()
            hf.close()

            strip = None
            for cookie in map(strip, h_lines[0].split(',')):
                (key, value) = cookie.split('=')

                if key == "public":
                    if value == "True":
                        ispublic = True
                    else:
                        ispublic = False

                if key == "type":
                    img_type = value

                if key == "width":
                    img_width = value

                if key == "height":
                    img_height = value

        else:  # ispublic, orignal image path
            # store relative path in database
            h_lines = ["""public={},type={},width={},height={}"""
                       .format(ispublic, img_type, img_width, img_height), tmp_img_path]


    # apply filter
    if "filter" in form:
        fil = form.getvalue("filter")

        tmp_img_path = tmp_img_dir + datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S-%f")\
            + "." + img_type

        if fil == "border":
            filters.border(h_lines[1], tmp_img_path,  "Black", "2x2")
        elif fil == "lomo":
            filters.lomo(h_lines[1], tmp_img_path)
        elif fil == "lens":
            filters.lens_flare(h_lines[1], tmp_img_path, img_width, img_height)
        elif fil == "blackwhite":
            filters.black_white(h_lines[1], tmp_img_path, img_width, img_height)
        elif fil == "bur":
            filters.blur(h_lines[1], tmp_img_path)
        else:  # no filter
            Image.open(h_lines[1]).save(tmp_img_path)

        h_lines.append(tmp_img_path)


    if "undo" in form and len(h_lines) > 2:
         # remove latest
        latest = h_lines[len(h_lines) - 1]
        h_lines.remove(latest)
        
        try:
            os.remove(latest)
        except:
            pass

    elif "discard" in form:
        # delete temporary files
        try:
            for i, hl in enumerate(h_lines, 0):
                if i != 0:
                    os.remove(hl)  # remove images
        except:
            pass

        os.remove(history)

        # extit to index page
        print(util.html_redirect("index.cgi"))
        sys.exit()


    elif "finish" in form:
        img_dir = "/img/"

        latest = h_lines[len(h_lines) - 1]

        img_path = latest.replace(tmp_img_dir, img_dir)
        img_path = img_path.replace(os.path.abspath(""), "")

        os.rename(latest, img_path.replace("/img/", "img/"))

        it = ImageTable()

        if it.insert((user, img_path), ispublic):
            pass

        try:
            h_lines.remove(latest)

            for i, hl in enumerate(h_lines, 0):
                if i != 0:
                    os.remove(hl)  # remove image

        except:
            pass

        os.remove(history)  # remove history

        # exit to index page
        print(util.html_redirect("index.cgi"))
        sys.exit()

    else:
        pass


    if write_history:
        # write history
        hf = open(history, 'w')
        for l in h_lines:
            hf.write(l + "\r\n")

        hf.close()

    # if False:
    #     try:
    #         public = form.getvalue("public")

    #         fstorage_name = str(datetime.datetime.now())

    #         fstorage_name = fstorage_name.replace(":", "-")
    #         fstorage_name = fstorage_name.replace(" ", "_")
    #         fstorage_name = fstorage_name.replace(".", "-")

    #         root_path = img_path + fstorage_name

    #         fn = os.path.basename(fileitem.filename)

    #         if not fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
    #             message = 'Failed to upload file: ' + fn + '\r\nInvalid ending'

    #         else:
    #             open(os.path.abspath("") + root_path,
    #                  'wb').write(fileitem.file.read())

    #             it = ImageTable()
    #             if it.insert((user, root_path), public):
    #                 message = 'The file "' + fn + '" was uploaded successfully'
    #             else:
    #                 message = 'Failed to upload file: ' + fn

    #     except Exception as err:
    #         message = 'Failed to upload file'
    #         pass

    if len(h_lines) < 3:
        undo_disable_str = "disabled"
    else:
        undo_disable_str = ""

    host = ""
    if os.environ.has_key("ASSIGNMENT1_SERVICE_HOST"):
        host = "http://root-csci4140-projects.a3c1.starter-us-west-1.openshiftapps.com"

    path = h_lines[len(h_lines) - 1].replace(os.path.abspath("") , "")

    print("""\
    Content-Type: text/html\n
      <html>
        <body>
          <img src="{}{}" alt="HTML5 Icon" style="height: 100%; width: 100%; max-width: 400px; max-height: 400px">
          <form enctype="multipart/form-data" action="index.cgi" method="post">  
            <p>Filter:     
            <input type="hidden" name="userID" value="{}"></input>
            <input type="hidden" name="action" value="upload"></input>
            <select onchange="this.form.submit()" name="filter">
              <option value="f_init">Choose</option>
              <option value="no_filter">None</option>
              <option value="border">Border</option>
              <option value="lomo">Lomo</option>
              <option value="lens">Lens Flare</option>
              <option value="blackwhite">Black White</option>
              <option value="bur">Bur</option>
            </select>        
          </form>
          <form action="index.cgi" method="post">
            <input type="hidden" name="action" value="upload"></input>
            <p>
            <button type="submit" name="discard" value="df">Discard</button> 
            <button type="submit" name="undo" value="dd" {}>Undo</button> 
            <button type="submit" name="finish" value="xc">Finish</button> 
            </p>
            <input type="hidden" name="userID" value="{}"></input>
          </form>  
        </body> 
      </html>
    """.format(host, path, user, undo_disable_str, user ))
