

from pymongo import MongoClient




def setFirstLast():
    c = MongoClient()

    for x in c.ratemt.Collections.find():
        a = x["name"].split(" ")
        if len(a) > 1:
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"first":a[0],"last":a[1]}})
        else:
            c.ratemt.Collections.update({"id":x["id"]},{"$set":{"first":a[0],"last":""}})


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
                c.ratemt.Collections.update({"id":k["id"]},{"$set":{"matched":True}})
            
            else:
                k = c.ratemt.Collections.find({"last":x["last"],"matched":False})
                if k.count() == 1:
                    close.append([x,k])
                else:
                    k = c.ratemt.Collections.find({"first":x["last"],"last":"","matched":False})
                    if k.count() == 1:
                        close.append([x,k])
                    else:
                        no.append(x)

    for x in no:
        print("%s %s"%(x["first"],x["last"]))



    print("%d perfect matches"%(len(perfect)))
    print("%d close matches"%(len(close)))
    print("%d no matches"%(len(no)))
          


if __name__ == "__main__":
    go()
#    setFirstLast()
