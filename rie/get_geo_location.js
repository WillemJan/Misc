var start_stop_btn, wpid=false, map, z, op, prev_lat, prev_long, min_speed=0, max_speed=0, min_altitude=0, max_altitude=0, distance_travelled=0, min_accuracy=150, date_pos_updated="", info_string="";

function format_time_component(time_component)
{
 if(time_component<10)
  time_component="0"+time_component;
 else if(time_component.length<2)
  time_component=time_component+"0";
  
 return time_component;
}

function geo_success(position)
{
 
 info_string="";
 var d=new Date(); 
 var h=d.getHours();
 var m=d.getMinutes();
 var s=d.getSeconds();
  
 var current_datetime=format_time_component(h)+":"+format_time_component(m)+":"+format_time_component(s);
  
 if(position.coords.accuracy<=min_accuracy)
 {
  if(prev_lat!=position.coords.latitude || prev_long!=position.coords.longitude)
  {
   if(position.coords.speed>max_speed)
    max_speed=position.coords.speed;
   else if(position.coords.speed<min_speed)
    min_speed=position.coords.speed;
    
   if(position.coords.altitude>max_altitude)
    max_altitude=position.coords.altitude;
   else if(position.coords.altitude<min_altitude)
    min_altitude=position.coords.altitude;
   
   
   prev_lat=position.coords.latitude;
   prev_long=position.coords.longitude;
   
   
   info_string="?lat="+position.coords.latitude+"&long="+position.coords.longitude+"&accuracy="+Math.round(position.coords.accuracy, 1)+"&speed_min="+(min_speed?min_speed:"0")+"&speed_max="+(max_speed?max_speed:"0")+"&altitude_min="+(min_altitude?min_altitude:"0")+"&altitude_max="+(max_altitude?max_altitude:"0")+"&accuracy="+Math.round(position.coords.altitudeAccuracy,1)+"&date="+current_datetime;
  }
 }
 else
  info_string="?date="+current_datetime;

 if(info_string) {
var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"] 
 if (window.ActiveXObject){ 
  for (var i=0; i<activexmodes.length; i++){
   try{
    var req= ActiveXObject(activexmodes[i]);
   }
   catch(e){
   }
  }
 }
 else if (window.XMLHttpRequest) {
        var req=new XMLHttpRequest;
}


 req.open('GET' , 'pos.cgi'+info_string,true);
    req.onreadystatechange = function (aEvt) {
    if (req.readyState == 4) {
       if(req.status == 200) { 
        document.getElementById('mes').innerHTML=req.responseText.split("|")[0];
        if ((document.getElementById('mes').innerHTML.search('not')) < 0) {
        document.getElementById('map').innerHTML='<iframe src="'+req.responseText.split("|",2)[1]+'" width=400 height=400 scolling=no"></iframe>';
        }

       }
       else
        alert("Error loading page\n");
    }
  };

 req.send(null);


}
}

function geo_error(error)
{
}


function get_pos()
{
 if(!!navigator.geolocation)
  wpid=navigator.geolocation.watchPosition(geo_success, geo_error, {enableHighAccuracy:true, maximumAge:30000, timeout:27000});

}


function init_geo()
{
  
    if(wpid) 
    {
     navigator.geolocation.clearWatch(wpid);
     wpid=false;
    }
    else 
    {
     get_pos();
    }
}

window.onload=init_geo;
