import os, web, time, urllib, hashlib 
from europeana.api import API
from mako.template import Template
import simplejson
import urllib2
import random


results = """\
<html>
<head>
<script type="text/javascript" src="http://www.lokaal.lan/jquery/jquery.js"></script>
<script type="text/javascript" src="http://www.lokaal.lan/jquery-ui.js"></script>
<script type="text/javascript" src="http://www.lokaal.lan/ui/jquery.ui.core.js"></script>
<script type="text/javascript" src="http://www.lokaal.lan/ui/jquery.ui.effects.core.js"></script>

<style>
body, div, span, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, code, del, dfn, em, img, q, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, dialog, figure, footer, header, hgroup, nav, section {margin:0;padding:0;border:0;font-weight:inherit;font-style:inherit;font-size:100%;font-family:inherit;vertical-align:baseline;}
i { font-size: 12px; }
input[type=text], input[type=password], input.text, input.title, textarea {background-color:#fff;border:1px solid #bbb;font-size: 20px;margin-left: 320px;}

body { overflow: hidden;} 
.results { margin: 0 auto;border-style:solid;border-width: 1px;margin: 5px;padding: 5px;  }
.result { border-style: solid; border-width: 1px; margin: 5px; height: 120 ;display:block;float: left; width: 120px;padding: 5px; backgound-color: black;}
.detail { clear: both; padding: 20px; height: 140px; overflow: hidden;}
</style>
<title>
${keyword}
</title>
</head>

<body>

<div class="results">
<img src="http://www.lokaal.lan/eu-labs.png" style='float: right;' height=40>
<h3 style='float:right; font-weight: bold'>RiE <font style="font-size: 11px;">(tm)</font></h3>
<form action="/result/" method="get" name=go>
<input type=text value="${keyword}" name="q" id="q" size=30>
</form>
<%
import time,urllib
now = time.time()
%>
% if numfound == 0:
    None found, for keyword : ${keyword} in ${round(now - elapse, 2)}
% elif numfound == 1:
    Found 1 record. ${keyword} in <i>${round(now - elapse, 2)}</i>
% else:
    <center> Found <b>${str(numfound)}</b>records for keyword <b>${keyword}</b> in <i>${round(now - elapse, 2)}</i> seconds.</center>
% endif
</div>
<div class="detail">

</div>

<br/>
% for item in records:
<div class="result" id="resultdiv-${item["counter"]}">
<img id="result-${item["counter"]}" src="http://www.lokaal.lan/ui-anim_basic_16x16.gif" style='float:right;width:16px;height:16px;margin: 10px;' onClick="document.go.submit()"> 
% for k in item.keys():
% if k == "link":
<script>


$.ajax({
  url: '/get/${urllib.quote(item[k])}',
  success: function(data) {
      var json = eval('('+data +')');
      $("#result-${item["counter"]}").attr("src",json["object"]);
      $("#result-${item["counter"]}").height(100);
      $("#result-${item["counter"]}").width(100);

      $("#result-${item["counter"]}").mouseover(function() {
        var keyword = json["word"][Math.floor(Math.random()*json["word"].length)]
        $("#q").val(keyword);
        $(".detail").html("<a href='"+json["uri"]+"'>View object<a/><br/><b>titile</b> "+json["title"]+"<br/><b>description</b> "+json["description"]+"<br><b>subject</b> "+json["subject"]);
        $("#result-${item["counter"]}").css("background-color")="red";

      });

      console.debug(json);
  }
});

</script>
    
% endif
% endfor 
</div>
% endfor 

<body>


</html>
"""


urls = ("/get/(.*)", "get", "/result/(.*)", "query", "/.*" ,"query")
app = web.application(urls, globals())

class get:
    def __init__(self):
        self.api= API()
    def GET(self,path):

        url=self.api.get_parse_europeana_object(path)
        words = []
        for word in url["description"].split(' ')+url["title"].split(' '):
            if len(word) > 4:
                if word.isalpha():
                    words.append(word)
        url["word"] =  words
        if "object" in url.keys():
            try:
                f = urllib2.urlopen(url["object"],timeout=1)
                if "content-type" in f.headers.keys():
                    return(simplejson.dumps(url))
            except:
                url["object"] = "http://www.lokaal.lan/blackcat.gif"
        else:
            url["object"] = "http://www.lokaal.lan/blackcat.gif"
        return(simplejson.dumps(url))


class query:
    def __init__(self):
        pass

    def GET(self, path=None):

        if not path.find('/') > -1:
            web.header('Content-Type','text/html; charset=utf-8', unique=True) 
            self.api = API()
            i = web.input()
            if "q" in i.keys():
                path=i["q"]
            if path:
                now=time.time()
                self.api.query(path, False)
                return(Template(results, default_filters=['unicode'],input_encoding='utf-8').render_unicode(numfound=self.api.numfound, records=self.api.records, elapse=now, keyword=path ))
        else:
            now=time.time()
            page = int(path.split('/')[0])
            query = path.split('/')[1]
            return(simplejson.dumps())


        return 'Hello, world!'


if __name__ == "__main__":
    app.run()
