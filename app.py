

from flask import Flask, render_template, request

import stuyteachers
import html


app = Flask(__name__)


@app.route("/")
def index():
    r = '<table>'
    r += '<tr><td>'+html.table_overpaid(5)+'</td><td style="padding-left:20px;">'+html.table_underpaid(5)+'</td></tr>'
    r += '<tr><td>'+html.table_highestpaid(5)+'</td><td>&nbsp;</td></tr>'
    r += '</table>'
    return render_template("search.html",table=r)


@app.route("/stuylist")
def stuylist():

    r = html.table_get("salary",-1,20,0)
    
    return render_template("search.html",table=r)

#    return render_template("teacher.html",first="Mike",last="zamansky")

@app.route("/json")
def json():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run()
