<%include file="header.html"/>

<div id="container1"> 
<font size="10">a</font>
%for i in range(1,26):
    <% j=(chr(97+int(i))) %>
    ${j}
%endfor

%for i, country in enumerate(sorted(g.factbook.keys())):
%if i<10:

<div id="container"> 
<a href="">
<img src="${g.factbook[country]["image"]}"><h4>${g.factbook[country]["fullname"]}</h4> 
</a>
<p>
Population : 

<br>
Size :<br>
</p>
</div>

%endif
%endfor
</div>
<%include file="footer.html"/>
