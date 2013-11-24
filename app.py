

from flask import Flask, render_template

import stuyteachers

app = Flask(__name__)


@app.route("/")
def index():
    r = ""
    s = stuyteachers.get("last")


    r = "<table>"
    for x in s:
        r += '<tr><td>%(first)s %(last)s</td><td>%(title)s</td>'%(x)

        if x["salary"] == -1:
            r += '<td><em>No Results</em></td>'
        else:
            r += '<td>$%(salary)d</td>'%(x)
   
        if len(x["address"]) > 0:
            r += '<td><strong>%s</strong><br />%s</td>'%(x["address"][0]["address"],x["address"][0]["phoneNum"])
        else:
            r += '<td>No address found</td>'

        r += '</tr>'

    r += "</table>"

    return r


if __name__ == "__main__":
    app.debug = True
    app.run()
