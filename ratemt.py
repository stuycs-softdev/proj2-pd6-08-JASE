import urllib
from bs4 import BeautifulSoup
from operator import itemgetter

def getRatings():
    results = getPageRatings("")
    x = 2
    prev = []
    while True:
        temp = getPageRatings("/%d" %(x))
        if prev == temp:
            break
        results += temp
        prev = temp
        x += 1
    return results

def getPageRatings(page_num):
    results = []

    url = "http://www.ratemyteachers.com/stuyvesant-high-school/13765-s" + page_num

    page = BeautifulSoup(urllib.urlopen(url))

    for x in page.find("table").find_all("tr"):
        if len(x.find_all("td")) > 0:
            a = x.find_all("td")
            name = a[0].find("span").get_text()
            overall = a[1].find("span").get_text()
            subject = a[2].get_text()
        
            results.append({"name":name, "overall":overall, "subject":subject})

    return results


if __name__ == "__main__":
   print(getRatings())
