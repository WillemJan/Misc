"""
    This file is part of Europeana Random Image Explorer.

    Copyright (C) 2011 Willem Jan Faber, Koninklijke Bibliotheek - National Library of the Netherlands

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

results = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<script type="text/javascript" src="${baseurl}jquery.js"></script>
<script type="text/javascript" src="${baseurl}maxSize.js"></script>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
<style type="text/css">
body, div, span, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, code, del, dfn, em, img, q, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, dialog, figure, footer, header, hgroup, nav, section {margin:0;padding:0;border:0;font-weight:inherit;font-style:inherit;font-size:100%;font-family:inherit;vertical-align:baseline;}
i { font-size: 12px; }
input[type=text], input[type=password], input.text, input.title, textarea {background-color:#fff;border:1px solid #bbb;font-size: 20px;margin-left: 0;width: 450px;clear:left; text-align: center;}
form { margin: 0 auto; }

body { overflow: hidden; font: 13px Verdana,Arial,'Bitstream Vera Sans',Helvetica,sans-serif;} 
.result { border-style: solid; border-width: 1px; margin-left: 10px; height: 120;display:block;float: left; width: 120px;padding: 4px; text-align: center; -moz-border-radius: 5px; border-radius: 5px;}
.detail { clear: both; padding: 20px; height: 400px; overflow: scroll; text-align: left;}
.contain { margin: 0 auto; width: 1000px;}
.search { margin: 0 auto;border-style: solid;border-width: 1px;margin: 5px;padding: 5px; width: 100%}
</style>
<title>
RiE@${keyword.replace(' OR ',' ')}
</title>
<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon" />
</head>
<body>
<div class="search">
<a href='http://europeanalabs.eu/wiki/EuropeanaOpenSearchAPI'><img src="${baseurl}europeana.png" style='float: right;' height="70" alt=""/></a>
<h3 style='float:right; font-weight: bold'><a href='/static/about.html'>RiE</a></font></h3>
<center>
<form action="/" method="get" name="go">
<input type="text" value="${keyword.replace(' OR ', ' ')}" name="q" id="q" size="30" />
</form>
</center>
<%
import time,urllib
%>
% if numfound == 0:
    None found, for keyword : ${keyword} in ${round(done-now, 2)}
% elif numfound == 1:
    Found 1 record. ${keyword} in <i>${round(done-now, 2)}</i>
% else:
    <center> Found <b>${str(numfound)}</b> records for keyword <b>${keyword.replace(' OR ',' ')}</b> in <i>${round(done -now, 2)}</i> seconds.</center>
% endif
</div>
<% 
api.randomize()
%>
<br/>
<div class="contain">
% for item in api.records:
<div class="result" id="resultdiv-${item["counter"]}">
<img class="euro" id="result-${item["counter"]}" onClick="$('.euro').hide();$('.spin').fadeIn();document.go.submit();" style='max-width: 100px; max-height: 100px; margin: auto;display: block;'/> 
<img src="${baseurl}spinner.gif" style='display: none;float:right;width:16px;height:16px;margin-top: 10px;margin-right: 50px;' onClick="document.go.submit()" id="spinner-${item["counter"]}" class="spin"> 

</div>
% for k in item.keys():
% if k == "link":
<script>
$("#spinner-${item["counter"]}").fadeIn();
$("#result-${item["counter"]}").hide();
$.ajax({
  url: '/get/${urllib.quote(item[k])}',
  success: function(data) {
    var json = eval('('+data +')');
    $("#spinner-${item["counter"]}").hide();
    $("#result-${item["counter"]}").attr("src","http://europeanastatic.eu/api/image?uri="+json["object"]+"&size=BRIEF_DOC&type=IMAGE");
    $("#result-${item["counter"]}").css("max-width",100);
    console.debug(json);
    $("#result-${item["counter"]}").fadeIn();
    $("#resultdiv-${item["counter"]}").mouseover(function() {
    if (Math.floor(Math.random()*10) > 5 ) {
        var keyword = json["word"][Math.floor(Math.random()*json["word"].length)];
    } else {
        var r = Math.floor(Math.random()*json["word"].length);
        var keyword = json["word"][r];
        var ro = r;
        var i = 0;
        while (ro == r) {
            r = Math.floor(Math.random()*json["word"].length);
            if (i > 10) break;
            i = i + 1;
        }
        keyword = keyword+" " + json["word"][r];
    };

    $("#q").val(keyword);
    $(".detail").html("<img style='float:right' src='http://europeanastatic.eu/api/image?uri="+json["object"]+"&size=FULL_DOC&type=IMAGE'>");

    for (var key in json ) {
        if ( (json[key].indexOf('http://') >= 0 ) &! (json[key].indexOf('(http://') >= 0 ))  {
          $(".detail").append("<p style='width:140px;float:left;font-weight:bold'><b>key</b></p><a href='"+json[key]+"'>"+key+"</a><br/>");
        } else {
          $(".detail").append("<p style='width:140px;float:left;font-weight:bold'>"+key+"</p>"+json[key]+"<br/>");
        }
    }
    $(".detail").append("<br/><br/>");
    $(".detail").append("<br/><br/>");


    } );
  }
});

</script>
    
% endif
% endfor 
% endfor 
<div class="detail">

</div>
</div>
<noscript>Please turn on JavaScript..</noscript>
<body>


</html>
"""


