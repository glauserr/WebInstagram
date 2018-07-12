#! /usr/bin/env python

import os

def html_redirect(file, waittime=0, html_body=""):
	return """
		<html>
		  <head>
		  <meta http-equiv="refresh" content="{}; /cgi-bin/{}">
		  <meta name="keywords" content="automatic redirection">
		</head>
		<body>{}</body>
		</html>
		""".format(waittime,file, html_body)


def html_redirect_with_button(file, button_msg, waittime=0, html_body=""):
	to_page = file
	return """
		<html>
		  <head>
		  <meta http-equiv="refresh" content="{}; /cgi-bin/{}">
		  <meta name="keywords" content="automatic redirection">
		</head>
		<body>
		  <p>{}</p>
		  <form method="post">
            <button type="submit" formaction="{}">{}</button>
          </form>
		</body>
		</html>
		""".format(waittime,to_page, html_body, to_page, button_msg)