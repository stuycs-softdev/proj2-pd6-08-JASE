
import stuyteachers

def table_overpaid(limit):
    r = '<table><tr><th colspan="4" style="text-align:center;">Top '+str(limit)+' Overpaid Teachers</td></tr><tr><th>&nbsp;</th><th>Teacher Name</th><th>Salary</th><th>Overall Rating</th></tr>'

    count = 0
    for x in stuyteachers.get_overpaid(limit):
        count += 1
        r += '<tr><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a></td><td>$%(salary)d</td><td>%(rmt_overall)d&#37;</td></tr>'%(x)

    r += '</table>'

    return r

def table_underpaid(limit):
    r = '<table><tr><th colspan="4" style="text-align:center;">Top '+str(limit)+' Underpaid Teachers</td></tr><tr><th>&nbsp;</th><th>Teacher Name</th><th>Salary</th><th>Overall Rating</th></tr>'

    count = 0
    for x in stuyteachers.get_underpaid(limit):
        count += 1
        r += '<tr><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a></td><td>$%(salary)d</td><td>%(rmt_overall)d&#37;</td></tr>'%(x)

    r += '</table>'

    return r


def table_highest(param,title,limit):
    r = '<table><tr><th colspan="4" style="text-align:center;">Top %d - %s</td></tr><tr><th>&nbsp;</th><th>Teacher Name</th><th>%s</th></tr>'%(limit,title,title)

    count = 0
    for x in stuyteachers.get(param,-1,limit):
        count += 1
        r += '<tr><td>'+str(count)+'</td><td><a href="teacher-%(id)d">%(first)s %(last)s</a></td>'%(x)

        info = str(x[param])
        if param == "salary":
            info = "$"+info
        elif param == "rmt_overall":
            info += "%"

        r += '<td>'+info+'</td></tr>'

    r += '</table>'

    return r
