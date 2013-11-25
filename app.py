

from flask import Flask, render_template, request
from pymongo import MongoClient
import json

import stuyteachers
import html


app = Flask(__name__)
c = MongoClient()

fname = "data.txt"

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

        r += '<div class="alert alert-info">Teacher value calculated as the ratio between salary and <strong>ratemyteachers.com</strong> overall rating</div>'
        r += '<table style="width:100%">'
        r += '<tr><td>'+html.table_overpaid(5)+'</td><td style="padding-left:20px;">'+html.table_underpaid(5)+'</td></tr>'
        r += '<tr><td>'+html.table_highestpaid(5)+'</td><td>&nbsp;</td></tr>'
        r += '</table>'
    return render_template("search.html",table=r)


@app.route("/stuylist")
def stuylist():

    r = html.table_get("last",1,20,0)
    
    return render_template("search.html",table=r)

#    return render_template("teacher.html",first="Mike",last="zamansky")

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

    return "Preload successful<br /><br /><a href='/'>Go Home</a>"

@app.route("/backup")
def backup():

    if c.teachers.Collections.count() > 0:
        f = open(fname,"w")

        a = []
        for x in c.teachers.Collections.find():
             a.append(x)

        f.write(json.dumps(a))

        return "Backup successful<br /><br /><a href='/'>Go Home</a>"

@app.route("/loadall")
def loadall():
    stuyteachers.teachersToDatabase()

    return "Load successful<br /><br /><a href='/'>Go Home</a>"


if __name__ == "__main__":
    app.debug = True
    app.run()
