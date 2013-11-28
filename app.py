

from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import json

import stuyteachers
import html
import gmap

app = Flask(__name__)
c = MongoClient()

fname = "data.txt"


def num(a):
    return '{:,.0f}'.format(a)



@app.route("/")
def index():

    r = ""

    if c.teachers.Collections.count() == 0:
        r += """
<div style="text-align:center;">
<h1>Attention</h1>
<h3>No teacher data has been found in the database.</h3>
</div>
<div style="margin-left:20%;margin-right:20%;width:60%;">


<div class="alert alert-success">
<div style="text-align:center;"><a href="/preload" class="btn btn-success btn-lg">Load from .txt file</a></div><br />
For your convenience, all teacher data has been preloaded using the option below and has been saved a .txt file beforehand.  To begin using <strong>StalkMyTeachers</strong> immediately you should click the above link to fill the database with all the information.<br /><br />
<em>If you are reviewing this project this is the suggested method.</em>
</div>

<div class="alert alert-warning">
<div style="text-align:center;"><a href="/loadall" class="btn btn-warning btn-lg">Load from online</a></div><br />
<div class="alert alert-danger"><strong>Warning:</strong> This option will take about 15-35 minutes</div><br />
Clicking the above will search the internet for information about every teacher.  This will load roughly a thousand webpages to search for information and takes quite some time.  If you close your browser while using this option all information will be lost.
</div>

</div>"""

    
    else:

        try:
            a = request.args.get("type")
            if a:
                r += '<div class="alert alert-success"><strong>Success:</strong> '

                if a == "1":
                    r += 'Data has been successfully loaded from .txt file into MongoDB.  Please enjoy using <strong>StalkMyTeachers</strong>!'
                elif a == "2":
                    r += 'Data has been successfully backed up into data.txt'
                r += '</div>'
        except:
            pass

        r += '<div class="alert alert-info">Teacher value calculated as the ratio between salary and <strong>ratemyteachers.com</strong> overall rating</div>'

        r += """
<div class="alert alert-info" style="text-align:left;">
There are <strong>%d</strong> teachers and faculty members <em>(Only <strong>%d</strong> have salary information available and only <strong>%d</strong> have ratemyteachers.com information available)</em>
<br />Combined yearly salary: <strong>$%s</strong>
<br />Average salary: <strong>$%s</strong>
<br />Average ratemyteachers.com rating: <strong>%d&#37;</strong>
</div>
"""%(stuyteachers.num_teachers(),stuyteachers.num_teachers({"salary":{"$ne":-1}}),stuyteachers.num_teachers({"rmt_overall":{"$ne":-1}}),num(stuyteachers.total_salary()),num(stuyteachers.average_salary()),stuyteachers.average_rmt())

        r += '<table style="width:100%">'
        r += '<tr><td>'+html.table_overpaid(5)+'</td><td style="padding-left:20px;">'+html.table_underpaid(5)+'</td></tr>'
        r += '<tr><td>'+html.table_highestpaid(5)+'</td><td style="padding-left:20px;">'+html.table_highest("rmt_overall","Top 5 Highest Rated Teachers","Overall Rating",5)+'</td></tr>'
        r += '</table>'
    return render_template("search.html",table=r,search=html.searchCode(request.args))


@app.route("/stuylist")
def stuylist():

    if len(request.args) == 0:
        r = html.table_get("last",1,20,0)
    else:
        r = html.table_search(request.args,20,0)
        
    
    return render_template("search.html",table=r,search=html.searchCode(request.args))

#    return render_template("teacher.html",first="Mike",last="zamansky")




# TEACHER PAGE
@app.route("/teacher-<n>")
def teacher(n):
    r = ""

    d = stuyteachers.get_teacher(int(n))

    if d != None:
        d['salary'] = num(d['salary'])
        r += """
<h1>%(first)s %(last)s</h1>

<div class="col-md-4">
<table class="table" style="border:1px solid rgb(221, 221, 221);">
<tr class="active"><th colspan="2" style="text-align:center;">Basic Information</td></tr>
<tr class="active"><td>First Name</td><td>%(first)s</td></tr>
<tr class="active"><td>Last Name</td><td>%(last)s</td></tr>
<tr class="active"><td>Title</td><td>%(title)s</td></tr>
<tr class="active"><td>Yearly Salary</td><td>$%(salary)s<br /><small>[As of year %(salary_year)s]</small></td></tr>"""%(d)

        if d["rmt_overall"] == -1:
            r += '<tr class="danger"><td colspan="2" style="text-align:center;font-weight:bold;">Ratemyteachers.com information unavailable</td></tr>'
        else:
            r += """
<tr class="active"><td>Ratemyteachers.com</td><td>
<table>
  <tr><td style="font-weight:bold;">Overall</td><td style="font-weight:bold;">%(rmt_overall)d&#37;</td></tr>
  <tr><td>Easiness</td><td> &nbsp; %(rmt_easiness)d</td></tr>
  <tr><td>Helpfulness</td><td> &nbsp; %(rmt_helpfulness)d</td></tr>
  <tr><td>Clarity</td><td> &nbsp; %(rmt_clarity)d</td></tr>
</table>
</td></tr>
"""%(d)

        r += """
</table>
</div>

<div class="col-md-8">
<table class="table">
<tr class="warning"><th colspan="2" style="font-weight:bold;text-align:center;">Address &amp; Phone Number Information<br />
<small><em>Click on a listing to display a Google Maps of the address</em></small></th></tr>"""

        if len(d["address"]) == 0:
            r += '<tr class="warning"><td colspan="2" style="text-align:center;">No Information Found</td></tr>'
        else:
            r += """
<tr class="warning"><td colspan="2">
<strong>Current Map:</strong><div id="curMap">%s</div><br />
<div style="text-align:center;">
<div class="btn-group">
<button type="button" onclick="mapZoomOut()" class="btn btn-default">-</button>
<button type="button" onclick="mapZoomIn()" class="btn btn-default">+</button>
</div>
<div class="btn-group">
<button type="button" onclick="mapRoadMap()" class="btn btn-default">Normal Map</button>
<button type="button" onclick="mapStreetView()" class="btn btn-default">Street View</button>
</div>

<br /><br />
<img src="%s" id="mapImg" />
</div>
</td></tr>"""%(d["address"][0]["address"],gmap.gmap(d["address"][0]["address"]))

            aw = "success"
            for x in d["address"]:
                r += '<tr class="%s mapListing"><td colspan="2"><a href="javascript:void(0)" style="font-weight:bold;">%s</a><br />%s</td></tr>'%(aw,x["address"],x["phoneNum"])
                aw = "warning"


        r += """

</table>
</div>
"""%(d)


    return render_template("search.html",table=r,search=html.searchCode({}))



# departments
@app.route("/department")
def department():
    r = ""

    r += """<table class="table table-striped table-bordered" id="depTable">
<tr class="active">
<th colspan="4" style="font-style:italic;text-align:center;">Click a column header below to sort</th>
</tr>
<tr class="active" class="col_heads active">
<th><a href="javascript:void(0)" onclick="sortDep(0,1)">Department</a></th>
<th><a href="javascript:void(0)" onclick="sortDep(1,-1)"># Teachers</a></th>
<th><a href="javascript:void(0)" onclick="sortDep(2,-1)">Average Salary</a></th>
<th><a href="javascript:void(0)" onclick="sortDep(3,-1)">Average Rating</a></th>
</tr>"""


    js = []

    for x in sorted(stuyteachers.get_departments()):
        k = stuyteachers.get_teachers_in_department(x)

        salary = []
        rating = []
        
        for y in k:
            if y["salary"] != -1:
                salary.append(y["salary"])
            if y["rmt_overall"] != -1:
                rating.append(y["rmt_overall"])
                
        sal = sum(salary)/len(salary)
        rat = sum(rating)/len(rating)


        r += '<tr><td><a href="stuylist?title=%s">%s</a></td><td><span>%d</span></td><td>$<span>%s</span></td><td><span>%d</span>&#37;</td></tr>'%(x.replace(" ","+"),x,len(k),num(sal),rat)
        js.append('["%s",%d,"%s",%d]'%(x,len(k),num(sal),rat))

    r += '</table>'

    r += '<script type="text/javascript">tab = ['+",".join(js)+'];</script>'

    return render_template("search.html",table=r,search=html.searchCode({}))





@app.route("/js")
def js():
    
    param = "last"
    sort = 1
    limit = 20
    offset = 0

    try:
        param = request.args.get("param")
        sort = request.args.get("sort")
        offset = request.args.get("offset")
    except:
        pass


    try:
        return str(html.table_get(param,sort,limit,int(offset)))
    except:
        return '{error:true}'


@app.route("/all")
def showAll():
    r = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Simple markers</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
    <script>

addr = ["""

    k = []

    for x in c.teachers.Collections.find():
        if len(x["address"]) > 0 and "lat" in x["address"][0]:
            k.append('["'+x["first"]+' '+x["last"]+'",'+str(x["address"][0]["lat"])+','+str(x["address"][0]["long"])+']')

    r += ",".join(k)

    r+= """];
function initialize() {
  var myLatlng = new google.maps.LatLng(40.7143528,-73.90597309999999);
  var mapOptions = {
    zoom: 13,
    center: myLatlng
  }
  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  for(x=0;x<addr.length;x++){
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(addr[x][1],addr[x][2]),
      map: map,
      title: addr[x][0]
    });
  }
}

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>
  <body>
    <div id="map-canvas"></div>
  </body>
</html>
"""
    return r




@app.route("/preload")
def preload():
    f = open(fname,"r")
    a = json.loads(f.read())#.replace("{u'",'{"').replace("'",'"'))

    for x in a:
        del x["_id"]

#    a = eval(f.read().replace("ObjectId(","").replace("'),","',"))

#    return str(a)


    if c.teachers.Collections.count() == 0:
        for x in a:
            c.teachers.Collections.insert(x)

    return redirect("/?type=1")#"Preload successful<br /><br /><a href='/'>Go Home</a>"

@app.route("/backup")
def backup():

    if c.teachers.Collections.count() > 0:
        f = open(fname,"w")

        a = []
        for x in c.teachers.Collections.find():
            x["_id"] = None
            a.append(x)

        f.write(json.dumps(a))

        return redirect("/?type=2")#"Backup successful<br /><br /><a href='/'>Go Home</a>"

@app.route("/loadall")
def loadall():
    stuyteachers.teachersToDatabase()

    return "Load successful<br /><br /><a href='/'>Go Home</a>"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5009)
