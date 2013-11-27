

######
## ANDREW ZARENBERG

## THIS IS MY TEST FILE

## NOBODY EDIT THIS

## THIS IS JUST FOR ME TO TEST FUNCTIONS
## THIS FILE DOES NOTHING

######

from pymongo import MongoClient
import json

import salary
import stuyteachers

def setFirstLast():
    c = MongoClient()

    for x in c.ratemt.Collections.find():
        a = x["name"].split(" ")
        if len(a) > 1:
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"first":a[0],"last":a[1]}})
        else:
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"first":"","last":a[0]}})


def go():
    c = MongoClient()

    for x in c.ratemt.Collections.find():
        if "id" in x.keys():
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"matched":False}})
    

    perfect = [] # perfect matches (first AND last)
    close = []   # close matches (last)
    no = []      # no matches

    for x in c.teachers.Collections.find():
        if "first" in x.keys() and "last" in x.keys():
            k = c.ratemt.Collections.find_one({"first":x["first"],"last":x["last"],"matched":False})

            if k:
                perfect.append(k)
                c.ratemt.Collections.update(
                    {"id":k["id"]},
                    {"$set":{
                            "matched":True,
                            "ratemyteachers":{
                                "overall":k["overall"],
                                "easiness":k["easiness"],
                                "helpfulness":k["helpfulness"],
                                "clarity":k["clarity"]#,
#                                "knowledgeable":k["knowledgeable"],
#                                "exam_difficulty":k["exam_difficulty"],
#                                "textbook_use":k["textbook_use"],
#                                "num_reviews":k["num_reviews"]
                                }
                            }
                     })
            
            else:
                k = c.ratemt.Collections.find({"last":x["last"],"matched":False})
                if k.count() == 1:
                    close.append([x,k])
                else:
                    k = c.ratemt.Collections.find({"first":"","last":x["last"],"matched":False})
                    if k.count() == 1:
                        close.append([x,k])
                    else:
                        no.append(x)


    print("Stuyvesant teachers matched with ratemyteachers.com results:")
    print("%d perfect matches"%(len(perfect)))
    print("%d close matches"%(len(close)))
    print("%d no matches"%(len(no)))
          



def printData():
    c = MongoClient()

    a = []
    for x in c.teachers.Collections.find():
        a.append(x)

    print(a)




def updateSalary():
    c = MongoClient()

    for x in c.teachers.Collections.find():
        sal = salary.getSalary(x['first'],x['last'])
        c.teachers.Collections.update({"id":x['id']},{"$set":{"salary":sal[0],"salary_year":sal[1]}})
        print("%s %s - $%d"%(x['first'],x['last'],sal[0]))


def fixSalary():
    c = MongoClient()

    for x in c.teachers.Collections.find():
        if x['salary'] != -1 and x['salary'] < 40000:
            c.teachers.Collections.update({"id":x['id']},{"$set":{"salary":-1,"salary_year":-1}})



def showTeachers():
    for x in stuyteachers.getTeachers():
        print(x["last"])



def ratings():
    c = MongoClient()

    for x in c.ratemt.Collections.find({"matched":False}):
        for y in c.teachers.Collections.find({"rmt_overall":-1,"last":{"$regex":x['last']+" "}}):
            print(y['first']+" "+y['last']+" = "+x['first']+" "+x['last'])





if __name__ == "__main__":
    ratings()
#    showTeachers()
#    updateSalary()
#    fixSalary()
#    printData()
#    go()
#    setFirstLast()
