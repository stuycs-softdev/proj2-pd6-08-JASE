

from flask import Flask, render_template

import stuyteachers

app = Flask(__name__)


@app.route("/")
def index():
    r = ""
    s = stuyteachers.get("salary",-1)
#    s = stuyteachers.get_overpaid(0)



    r = "<table>"
    count = 0
    for x in s:
        count += 1
        r += '<tr><td>'+str(count)+'</td><td>%(first)s %(last)s</td><td>%(title)s</td>'%(x)

        if x["salary"] == -1:
            r += '<td><em>No Results</em></td>'
        else:
            r += '<td>$%(salary)d</td>'%(x)
   
        if len(x["address"]) > 0:
            r += '<td><strong>%s</strong><br />%s</td>'%(x["address"][0]["address"],x["address"][0]["phoneNum"])
        else:
            r += '<td>No address found</td>'

        if x["rmt_overall"] == -1:
            r += '<td colspan="4">No ratings</td>'
        else:
            r += '<td>%(rmt_overall)s&#37;</td><td>%(rmt_easiness)d</td><td>%(rmt_helpfulness)d</td><td>%(rmt_clarity)d</td>'%(x)

        r += '</tr>'

    r += "</table>"

    return r


if __name__ == "__main__":
    app.debug = True
    app.run()
