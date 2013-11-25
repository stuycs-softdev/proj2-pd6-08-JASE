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
            overall = int(a[1].find("span").get_text()[:-1])
            subject = a[2].get_text()
            page_link = a[0].find("a")['href']
            

            page_link = "http://www.ratemyteachers.com" + page_link

            page2 = BeautifulSoup(urllib.urlopen(page_link))
           
            rlist = page2.find_all("ul", {"class" : "stars"})

            easiness = len(rlist[0].find_all("li", {"class" : "yellowStar"}))
            helpful = len(rlist[1].find_all("li", {"class" : "yellowStar"}))
            clarity = len(rlist[3].find_all("li", {"class" : "yellowStar"}))

            

            nreviews = int(page2.find("span", {"class" : "reviews"}).get_text()[:-8])


            results.append({"name":name, "overall":overall, "subject":subject, "easiness":easiness, "helpfulness":helpful, "clarity":clarity, "reviews":nreviews})

            print("%s (%s)\t%s, %d, %d, %d, %s"%(name,subject,overall,easiness,helpful,clarity, nreviews))

    return results


if __name__ == "__main__":
   print(getRatings())
