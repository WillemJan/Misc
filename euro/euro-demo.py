import os, web, time, urllib, hashlib 
from europeana.api import API
from mako.template import Template
import simplejson
import urllib2



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
input { font-size: 13px; font-weight: bold}
.results { margin: 0;padding: 0px;border-style:solid;border-width: 1px;margin: 0px;padding: 0px; overflow: hidden; }
.result { border-style: solid; border-width: 1px; margin: 0px; height: 100; width: 100px;display:block;float:left; }
.prev { height: 150px; } 
</style>
<title>
${keyword}
</title>
</head>

<body>

<div class="results">
<form action="/result/" method="get">
<input type=text value="${keyword}" name="q">
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
    Found <b>${str(numfound)}</b> records in <i>${round(now - elapse, 2)}</i> seconds.
% endif
</div>
<br/>
<div class="prev">

</div>


<div class="results">
% for i in range(0,20):
<div class="result" id="resultdiv-${i}">
<img id="result-${i}" src="http://www.lokaal.lan/ui-anim_basic_16x16.gif" style='float:right;width:16px;height:16px;'> 

<script>


$.ajax({
  url: '/result/json/1/appel',
  success: function(data) {
      $("#result-${i}").attr("src",data);
  }
});
</script>



</div> 
% endfor 

</div>


<body>


</html>
"""


urls = ("/result/(.*)", "query", "/.*" ,"query")
app = web.application(urls, globals())

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
            print(path)
            return()


        return 'Hello, world!'


if __name__ == "__main__":
    app.run()
