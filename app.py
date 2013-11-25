

from flask import Flask, render_template, request
import json

import stuyteachers
import html


app = Flask(__name__)


@app.route("/")
def index():
    
    r = ""

    r += '<div class="alert alert-info"><strong>Overall Rating</strong> information provided by <em>ratemyteachers.com</em></div>'
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

if __name__ == "__main__":
    app.debug = True
    app.run()
