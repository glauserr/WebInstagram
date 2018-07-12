#!/usr/bin/env python

import cgi
import cookies, util
from database import SessionTable

def logout(form):
	success = False

	if cookies.request_has_cookies():
		session_id = cookies.request_get_sessionID()

		st = SessionTable()
		if st.delete_session(session_id):
			success = True

	if success:
		print(cookies.delete_session_cookie()\
			  + "Content-Type: text/html; charset=utf-8\n\n"\
			  + util.html_redirect("index.cgi"))

	else:
		print("""
			Content-type: text/html\n\n
			<html>
			<body>
			<h1>Logout failed</h1>
			</body>
			</html>
			""")