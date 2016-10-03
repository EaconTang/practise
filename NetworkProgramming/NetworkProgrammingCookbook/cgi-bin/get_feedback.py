# -*- coding: utf-8 -*-
import cgi
import cgitb

form = cgi.FieldStorage()
name = form.getvalue("Name")
comment = form.getvalue("Comment")

output = """Content-type:text/html\r\n\r\n
<html>
<head>
<title>CGI program example</title>
</head>
<body>
<h2> {} send a comment: {} </h2>
</body>
</html>
""".format(name, comment)