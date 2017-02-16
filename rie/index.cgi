#!/usr/bin/env python

page = """

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="nl" lang="nl">
<head>
    <meta name="robots" content="all" /> 
    <meta name="description" content="Willem Jan Faber's Random Projects" />
    <meta name="author" content="Willem Jan Faber" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>~ Fe2.nl ~</title>
    <script type="text/javascript" src="get_geo_location.js"></script>
    <style type="text/css">
    body {
        font: 80% arial, sans-serif;
        background: #000000;
        margin: 0px;
        color: #ffffff;
    }
    a:link, a:visited, a:focus {
        color: #00c;
        text-decoration: none;
        font-family: "Lucida Grande","Lucida Sans Unicode",Arial,Verdana,sans-serif;
    }
    a:active {
        color: red;
    }
    </style>
</head>
<body bgcolor="#000">
<br> <br> <br> <br> <br>
<br> 

<h1 style='text-align: center;color:fff;' id='mes'>Trying to determine location</h1>
<div id=map style='text-align:center;'>

</div>

<noscript>
    You need javascript to view this site.
</noscript>

The source code is <a href='https://fe2.nl/random_projects/#WhichYouAreHere'>Here!</a>

</body>
</html>
"""


print "Content-Type: text/html"
print

print (page)
