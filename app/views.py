# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, make_response, session
from app import app
from app.lib.AppExceptions import *
from app.lib.LocationSearch import LocationSearch

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

'''jsonData = { "Baltimore":{
    "health": {
      "hospital": {
        "data": {"frequency": 10, "relevance": 0.7845, "sentiment": "Mixed"},
        "metadata": {
          "article1": {"author": "Tom Jones", "title": "Current Rises in Health Insurance Policies in Baltimore", "timestamp": "26-FEB-1987 15:01:01.79"},
          "article2": {"author": "Bob Jenkins", "title": "Obamacare in Hospitals", "timestamp": "06-SEP-2011 16:32:34.73"},
          "article3": {"author": "Tom Jones", "title": "Rises in Hospital Fees", "timestamp": "31-DEC-1991 01:45:59.66"}
        } 
      } 
    },
    "crime": {
      "assault": {
        "data": {"frequency": 5, "relevance": 0.9045, "sentiment": "Negative"},
        "metadata": {
          "article1": {"author": "", "title": "Another shooting in Baltimore", "timestamp": "26-FEB-1987 15:01:01.79"},
          "article2": {"author": "Anderson Silva", "title": "Street Crime up in cities", "timestamp": "06-SEP-2011 16:32:34.73"},
          "article3": {"author": "John Jones", "title": "Rise in assaults in Baltimore", "timestamp": "31-DEC-1991 01:45:59.66"}
        } 
      },
      "robbery": {
        "data": {"frequency": 5, "relevance": 0.553, "sentiment": "Positive"},
        "metadata": {
          "article1": {"author": "Rob", "title": "Robbery of Museum in Baltimore", "timestamp": "26-FEB-1987 15:01:01.79"},
          "article2": {"author": "Anderson Silva", "title": "Man held at gunpoint for wallet", "timestamp": "06-SEP-2011 16:32:34.73"},
          "article3": {"author": "John Jenkins", "title": "Increase in robbery frequency in MD", "timestamp": "31-DEC-1991 01:45:59.66"}
        } 
      }       
    }
  }
}'''    

@app.route('/locationsearch', methods=['GET'])
def locationsearch():
    try:
        if request.args.has_key('prefix'):
            prefix = request.args['prefix']
            search_results = app.locationsearch.search(prefix)
            #return jsonify(status='success', results=search_results)
            return '''
<!DOCTYPE html>
<meta charset="utf-8">
<link href="../static/nv.d3.css" rel="stylesheet" type="text/css">
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.css" />
<link rel="stylesheet" href="../static/bootstrap.css" />
<style>

body {
  background: #fff;
  overflow-y:scroll;
}

text {
  font: 12px sans-serif;
}

.mypiechart {
  width: 500px;
  border: 2px;
}
#map { height: 200px; }

</style>
<head>
    <meta http-equiv="Content-Type"
      content="text/html; charset=utf-8"/>
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"
      type="text/javascript"></script>
    <script src="../static/js/jquery.tagcloud.js"
      type="text/javascript"></script>
       <script src="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.js" type="text/javascript"></script>
       <script src="../static/js/script.js"
      type="text/javascript"></script>
      <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?sensor=false"></script>
    <!-- <script src="custom.js"    
      type="text/javascript"></script> -->
</head>
<body class='with-3d-shadow with-transitions' onload="setupBlocks();">
<div  class="block">
<h2>Search:</h2>
<svg id="test1" class="mypiechart"></svg>
</div>
<div id="whatever" class="block">
<a href="" rel=7 onclick = "return Display('health')">health</a>
<a href="" rel=3 onclick = "return Display('crime')">crime</a>
<a href="" rel=10 onclick = "return Display('weather')">weather</a>
<a href="" rel=5 onclick = "return Display('employment')">employment</a>
</div>
<div id="map" class="block"></div>
<!--<h2>Test2</h2>
<svg id="test2" class="mypiechart"></svg>-->

<script src="../static/js/d3.v3.js"></script>
<script src="../static/js/nv.d3.js"></script>
<script src="../static/js/legend.js"></script>
<script src="../static/js/pie.js"></script>
<script src="../static/js/pieChart.js"></script>
<script src="../static/js/utils.js"></script>
<script src="http://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
<script>

  var testdata = [
    {
      key: "health",
      y: 0
    },
    {
      key: "crime",
      y: 0
    },
    {
      key: "weather",
      y: 0
    },
    {
      key: "employment",
      y: 0
    }
  ];

nv.addGraph(function() {
    var width = 500,
        height = 500;

    var chart = nv.models.pieChart()
        .x(function(d) { return d.key })
        .y(function(d) { return d.y })
        .color(d3.scale.category10().range())
        .width(width)
        .height(height);

      d3.select("#test1")
          .datum(testdata)
        .transition().duration(1200)
          .attr('width', width)
          .attr('height', height)
          .call(chart);

    chart.dispatch.on('stateChange', function(e) { nv.log('New State:', JSON.stringify(e)); });

    return chart;
});

var myJSONObject = ''' + str(jsonify(search_results)) + '''

var Position = '';
for (var y in myJSONObject){
  Position = y;
}
console.log(y);
//console.log(myJSONObject.Baltimore.health.hospital.data.frequency);



for (var y in myJSONObject){
testdata[0].y = objLength(myJSONObject[y].health);
testdata[1].y = objLength(myJSONObject[y].crime);
testdata[2].y = objLength(myJSONObject[y].weather);
testdata[3].y = objLength(myJSONObject[y].employment);
}
//console.log(testdata[0].y);

function objLength(obj){
  var i=0;
  for (var x in obj){
    if(obj.hasOwnProperty(x)){
      //console.log(obj[x]);
      i = i + obj[x].data.frequency;
    }
  } 
  return i;
}

function Display(obj){
  $('#whatever').empty();
  for (var x in myJSONObject[Position][obj]){
  $("#whatever").append(jQuery('<a>').attr({'href': 'url', 'rel': myJSONObject[Position][obj][x].data.frequency}).text(x));    
  }
  setupBlocks();
  $('#whatever a').tagcloud();
  setupBlocks();
  return false;
}
/*function get_values(obj){
  var i=0;
  for (var x in obj){
      if(obj.hasOwnProperty(x)){
         console.log(x); 
        }
}*/

//alert(objLength(myJSONObject.category.health));

/*for(var i = 0; i < objLength(myJSONObject); i++)
{
    for(var j = 0; j < objLength(myJSONObject.Baltimore); j++)
    {
        for (var x in myJSONObject.Baltimore)
            console.log(x);
    }
}*/
/*$("#whatever").append(jQuery('<a>').attr({'href': 'url', 'rel': 7}).text('bldh'));
key[0] = "Crime";
key[1] = "weather";
key[3] = "health";
for (index = 0; index < key.length; ++index) {
$("#whatever").append(jQuery('<a>').attr({'href': 'url', 'rel': index}).text(key[index]));      
}
//$("#whatever").append(jQuery('<a>').attr({'href': 'url', 'rel': 7}).text('blah'));/
*/


$.fn.tagcloud.defaults = {
  size: {start: 18, end: 22, unit: 'pt'},
  color: {start: '#2de', end: '#dee'}
};
$(function () {
  $('#whatever a').tagcloud();
});


var geocoder =  new google.maps.Geocoder();
    geocoder.geocode( { 'address': Position}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
            //alert(results[0].geometry.location.lat());
            //alert(results[0].geometry.location.lng());
            var loc = results[0].geometry.location,
            lat = loc.lat(),
            lng = loc.lng();
            showmap(lat,lng);
            //alert("location : " + results[0].geometry.location.lat() + " " +results[0].geometry.location.lng()); 
          } else {
            alert("Something got wrong " + status);
          }
        });

function showmap(lat, lng) {
  //console.log(lat, lng);
  //var map = L.map('map').setView([39.26, -76.61], 13);
//var marker = L.marker([39.26, -76.61]).addTo(map);
var map = L.map('map').setView([lat,lng], 13);
var marker = L.marker([lat,lng]).addTo(map);
L.tileLayer('http://{s}.tile.cloudmade.com/e66c31e8a69b402b8535b986af0e18a3/997/256/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    maxZoom: 18
}).addTo(map);
}

</script>
'''


        else:
            raise ParameterMissingException(expected=['prefix'], provided=request.args)
    except ParameterMissingException as error:
        return jsonify(status='error', msg=str(error))
