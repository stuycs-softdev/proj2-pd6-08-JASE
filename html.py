
import stuyteachers

def table_overpaid(limit):
    r = '<table class="table"><tr class="danger"><th colspan="4" style="text-align:center;">Top '+str(limit)+' Overpaid Teachers</td></tr><tr class="danger"><th>&nbsp;</th><th>Teacher Name</th><th>Salary</th><th>Overall Rating</th></tr>'

    count = 0
    for x in stuyteachers.get_overpaid(limit):
        count += 1
        r += '<tr class="danger"><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a><br /><small>%(title)s</small></td><td>$%(salary)d</td><td style="text-align:center">%(rmt_overall)d&#37;</td></tr>'%(x)

    r += '</table>'

    return r

def table_underpaid(limit):
    r = '<table class="table"><tr class="success"><th colspan="4" style="text-align:center;">Top '+str(limit)+' Underpaid Teachers</td></tr><tr class="success"><th>&nbsp;</th><th>Teacher Name</th><th>Salary</th><th>Overall Rating</th></tr>'

    count = 0
    for x in stuyteachers.get_underpaid(limit):
        count += 1
        r += '<tr class="success"><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a><br /><small>%(title)s</small></td><td>$%(salary)d</td><td style="text-align:center">%(rmt_overall)d&#37;</td></tr>'%(x)

    r += '</table>'

    return r


def table_highestpaid(limit):
    return table_highest("salary","Top "+str(limit)+" Highest Paid Teachers","Salary",limit)

def table_highest(param,table_title,column_title,limit):
    r = '<table class="table"><tr class="active"><th colspan="4" style="text-align:center;">%s</td></tr><tr class="active"><th>&nbsp;</th><th>Teacher Name</th><th>%s</th></tr>'%(table_title,column_title)

    count = 0
    for x in stuyteachers.get(param,-1,limit):
        count += 1
        r += '<tr class="active"><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a><br /><small>%(title)s</small></td>'%(x)

        info = str(x[param])
        if param == "salary":
            info = "$"+info
        elif param == "rmt_overall":
            info += "%"

        r += '<td>'+info+'</td></tr>'

    r += '</table>'

    return r


def table_get(param, sort, limit, offset=0):
    sort = int(sort)
    offset = int(offset)

    r = ""
    if offset == 0:
        r += """
<table class="table" id="sortTable">
  <tr class="active"><th colspan="5" style="font-style:italic;text-align:center;">Click a column header below to sort</th></tr>

  <tr class="col_heads active">
    <th>&nbsp;</th>
    <th><a href="javascript:void(0)" onclick="sort('last',1)">Name</a></th>
    <th><a href="javascript:void(0)" onclick="sort('salary',-1)">Salary</a></th>
    <th><a href="javascript:void(0)" onclick="sort('rmt_overall',-1)">Overall Rating</a></th>
    <th>Address and Phone Number</th>
  </tr>
"""

    count = offset
    for x in stuyteachers.get(param, sort, limit, offset):
        count += 1
        r += '<tr class="active"><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a><br /><small>%(title)s</small></td>'%(x)

        if x['salary'] != -1:
            r += '<td>$%(salary)d</td>'%(x)
        else:
            r += '<td style="font-style:italic;">No Data</td>'
        
        if x['rmt_overall'] != -1:
            r += '<td style="text-align:center;">%(rmt_overall)d&#37;</td>'%(x)
        else:
            r += '<td style="font-style:italic;text-align:center;">No Data</td>'

        if len(x['address']) > 0:
            r += '<td><strong>%s</strong><br />%s'%(x['address'][0]['address'],x['address'][0]['phoneNum'])
            if len(x['address']) > 1:
                r += '<br /><a href="javascript:void(0)" onclick="viewmore(this)">[Show '+str(len(x['address'])-1)+' other possible addresses]</a></td></tr><tr style="display:none" class="active" id="addr'+str(x["id"])+'"><td>&nbsp;</td><td colspan="4"><table>'
                for y in range(1,len(x['address'])):
                    r += '<tr><td style="font-weight:bold;">'+x["address"][y]["address"]+'</td><td style="padding-left:15px;">'+x["address"][y]["phoneNum"]+'</td></tr>'
                r += '</table></td></tr>'

            else:
                r += '</td></tr>'
        else:
            r += '<td>No address found</td></tr>'


    if offset == 0:
        r += '<tr id="loadMore" class="active"><td colspan="5" style="text-align:center;"><a href="javascript:void(0)" onclick="loadMore()">Load More Results</a><br /><br /><a href="#">Back to Top</a></td></tr>'


        r += '</table>'

    return r
