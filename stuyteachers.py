## ACCESS TEACHER LIST:
## getTeachers(SORT)
## available options:
## - first
## - last (DEFAULT if left blank)
## - title
##
## returns dictionary of sorted results


import urllib
import json
import math
from bs4 import BeautifulSoup
from operator import itemgetter

from pymongo import MongoClient


# our functions
import pFinder # gets addresses and phone numbers
import salary  # gets salary
import ratemt  # ratemyteachers.com

c = MongoClient()


# special cases
special = [
    # Department to be part of, Title
    ["Computer Science","Coordinator Comp Sci"]
]



def getTeachers(s=None):
    url = "http://stuy.enschool.org/apps/staff/"
    result = BeautifulSoup(urllib.urlopen(url))

    r = []
    for x in result.find("table").find_all("tr"):
        name = x.find("td").find("a")
        if name:
            n = name.get_text().split(". ")[1]#.split(" ")

            r.append({
                "first":n.split(" ")[0],
                "last":n.replace(n.split(" ")[0]+" ",""),
                "title":x.find_all("td")[1].get_text()
                })
                

    if r and s in r[0].keys():
        r = sorted(r, key=itemgetter(s))
    
    return r

def teachersToDatabase():
    c.teachers.Collections.remove()

    print("Adding in teachers to database...")
    
    teachers = getTeachers()
    for x in range(0,len(teachers)):
        t = teachers[x]
        t["id"] = x


        # add in teacher's salary
        gs = salary.getSalary(t["first"],t["last"])
        t["salary"] = int(gs[0])
        t["salary_year"] = int(gs[1])

        # array for multiple address results of teachers
        t["address"] = []
        addr = pFinder.pFind(t["first"],t["last"])

        if addr:
            for z in addr:
            # z["map"] = gmap()  --- placeholder for Google Maps function
                t["address"].append(z)

        t["rmt_overall"] = -1
        t["rmt_easiness"] = -1
        t["rmt_helpfulness"] = -1
        t["rmt_clarity"] = -1
        t["rmt_num_reviews"] = 0
            

        c.teachers.Collections.insert(teachers[x])

#        if t["salary"] == -1:
#            print("[%d] Error  %s %s"%(x,t["first"],t["last"]))
#        else:
        pr = "[%d]\t{{ %s %s }}\t"%(x,t["first"],t["last"])
        if t["salary"] == -1:
            pr += "Error "
        else:
            pr += "$%d"%(t["salary"])
        if(len(t["address"]) > 0):
            pr += "\t%s\t%s"%(t["address"][0]["phoneNum"],t["address"][0]["address"])
        else:
            pr += "No address found"
        pr += "\n"
        print(pr)



    do_ratemyteachers()

    print("Done.")
    



def fix_address(n):
    r = []
    
    for x in n:
        if "(212)" in x["phoneNum"] or "(718)" in x["phoneNum"] or "NeW York" in x["address"] or "Brooklyn" in x["address"]:
            r.append(x)
            n.remove(x)

    if len(r) > 0:
        return r
    return n




def do_ratemyteachers():
    c.ratemt.Collections.remove()
    # compare ratemyteachers
    print("Searching up results from ratemyteachers.com:")
    
    res = ratemt.getRatings()
    
    for x in range(0,len(res)):
        res[x]["id"] = x
        res[x]["overall"] = res[x]["overall"]
        c.ratemt.Collections.insert(res[x])




    # pair up with ratemyteachers
    for x in c.ratemt.Collections.find():
        a = x["name"].split(" ")
        if len(a) > 1:
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"matched":False,"first":a[0],"last":a[1]}})
        else:
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"matched":False,"first":"","last":a[0]}})

    

    perfect = [] # perfect matches (first AND last)
    close = []   # close matches (last)
    no = []      # no matches

    for x in c.teachers.Collections.find():
        if "first" in x.keys() and "last" in x.keys():
            k = c.ratemt.Collections.find_one({"first":x["first"],"last":x["last"],"matched":False})

            if k:
                perfect.append(k)
                teacher_update(x,k)
            
            else:
                k = c.ratemt.Collections.find({"last":x["last"],"matched":False})
                if k.count() == 1:
                    close.append([x,k])
                    teacher_update(x,k[0])
                else:
                    no.append(x)

    for x in c.ratemt.Collections.find({"matched":False}):
        for y in c.teachers.Collections.find({"rmt_overall":-1,"last":{"$regex":x['last']+" "}}):
            teacher_update(y,x)
#            print(y['first']+" "+y['last']+" = "+x['first']+" "+x['last'])



    print("Stuyvesant teachers matched with ratemyteachers.com results:")
    print("%d perfect matches"%(len(perfect)))
    print("%d close matches"%(len(close)))
    print("%d no matches"%(len(no)))




def teacher_update(x,k):
    c.ratemt.Collections.update({"id":k["id"]},{"$set":{"matched":True}})
    c.teachers.Collections.update(
        {"id":x["id"]},
        {"$set":{
                "rmt_overall":k["overall"],
                "rmt_easiness":k["easiness"],
                "rmt_helpfulness":k["helpfulness"],
                "rmt_clarity":k["clarity"]
                }
         })




def get(a,sort=1,limit=-1,offset=0,teachers=False):
    # sort:

    r = []


    k = c.teachers.Collections.find({a:{"$ne":-1}}).sort(a,sort).skip(offset)
    if teachers:
        count = 0
        for x in k:
            if "Teacher" in x['title']:
                r.append(x)
                count += 1
                if count == limit:
                    break
    else:
        if limit > 0 :
            k = k.limit(limit)
    
        for x in k: 
            r.append(x)

    return r



def search(ar,limit,offset=0):
    r = []


    
    temp = ""


    m = []




    if "name" in ar and ar.get("name") != "":
        temp = ar.get("name").replace(" ","|").replace("-","|")
        
        m.append({"$or":[
                    {"first":{"$regex":temp,"$options":"-i"}},
                    {"last":{"$regex":temp,"$options":"-i"}}
                    ]
                  })

    if "title" in ar and ar.get("title") != "":
        k = [{"title":{"$regex":ar.get("title"),"$options":"-i"}}]

        for x in special:
            if ar.get("title") == x[0]:
                k.append({"title":x[1]})

        if len(k) > 1:
            m.append({"$or":k})
        else:
            m.append(k[0])

#        k = c.teachers.Collections.find({
#                "$or":[
#                        {"first":{"$regex":temp,"$options":"-i"}},
#                        {"last":{"$regex":temp,"$options":"-i"}}
#                        ]
#                })

    
    if len(m) == 0:
        k = c.teachers.Collections.find()
    else:
        k = c.teachers.Collections.find({"$and":m})

    for x in k.sort("last",1):
        r.append(x)

    return r
    


def get_overpaid(limit):
    return get_payscale(limit,True,2,.65)
def get_underpaid(limit):
    return get_payscale(limit,False,.65,2)

def get_payscale(limit,order,b1,b2):
    a = []

    # salary and overall rating must be there
    for x in c.teachers.Collections.find({"salary":{"$ne":-1},"rmt_overall":{"$ne":-1}}):
        if x["rmt_overall"] != 0 and "Teacher" in x["title"]:
#            ratio = math.sqrt(x["salary"])/(x["rmt_overall"]*x["rmt_overall"])
            ratio = math.pow(x["salary"],b1)/math.pow(x["rmt_overall"],b2)

            a.append([ratio,x])

    a = sorted(a, key=itemgetter(0), reverse=order)

    r = []
    for x in range(min(limit,len(a))):
        r.append(a[x][1])

    return r




def get_departments():
    k = c.teachers.Collections.find({"title":{"$regex":"Teacher"}}).distinct("title")

    r = []
    for x in k:
        x = x.replace("Teacher ","").split(",")[0].split(" &")[0]

        spl = x.split("/")
        if len(spl) > 1:
            for y in spl:
                if y not in r:
                    r.append(y)
            
        else:

            if x not in r:
                r.append(x)

    return r


def get_teachers_in_department(n):
    r = []
    for x in c.teachers.Collections.find({"title":{"$regex":n}}):
        r.append(x)

    for x in special:
        if n == x[0]:
            for y in c.teachers.Collections.find({"title":x[1]}):
                r.append(y)

    return r




def get_teacher(n):
    return c.teachers.Collections.find_one({"id":n})

def num_teachers(a={}):
    return c.teachers.Collections.find(a).count()

def total_salary():
    sal = 0
    k = c.teachers.Collections.find({"salary":{"$ne":-1}})
    for x in k:
        sal += x['salary']
    return sal

def average_salary():
    sal = []
    k = c.teachers.Collections.find({"salary":{"$ne":-1}})
    for x in k:
        sal.append(x['salary'])
    return sum(sal)/len(sal)

def average_rmt():
    rmt = []
    k = c.teachers.Collections.find({"rmt_overall":{"$ne":-1}})
    for x in k:
        rmt.append(x['rmt_overall'])

    if len(rmt) > 0:
        return sum(rmt)/len(rmt)
    else:
        return 0


if __name__ == "__main__":
#    c = MongoClient()
#    c.ratemt.Collections.remove()
#    print("Searching up results from ratemyteachers.com:")
#    
#    res = ratemt.getRatings()
#    
#    for x in range(0,len(res)):
#        res[x]["overall"] = int(res[x]["overall"].replace("%",""))
#        res[x]["id"] = x
#        c.ratemt.Collections.insert(res[x])

#    teachersToDatabase()

#    for x in c.teachers.Collections.find():
#        c.teachers.Collections.update({"id":x["id"]},{"$set":{"address2":x["address"],"address":None}},upsert=True)

    for x in c.teachers.Collections.find():
        c.teachers.Collections.update({"id":x["id"]},{"$set":{"address2":[]}},upsert=True)

#    for x in c.teachers.Collections.find():
#        print("%s %s"%(x['first'],x['last']))
#        a = fix_address(pFinder.pFind(x["first"],x["last"]))
#        if len(a) > 0:
#            print(a[0]["address"].lstrip())
#            c.teachers.Collections.update({"id":x["id"]},{"$set":{"address":a}},upsert=True)

#    print(str(fix_address(pFinder.pFind("Mark","Halperin"))))

#    do_ratemyteachers()
