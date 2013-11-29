import urllib
import urllib2
from bs4 import BeautifulSoup
from operator import itemgetter
import sys



def zipinfo(zipcode):

    url = "http://zipwho.com/?zip=" + zipcode  + "&city=&filters=--_--_--_--&state=&mode=zip"

    request = urllib2.Request(url, headers={'User-Agent':"Magic Browser"})
    result = urllib2.urlopen(request)

    page = BeautifulSoup(result)
    
    x = page.find("script").get_text().split("\"")[1].replace('\\n',',').split(',')

    namenum = 0
    statnum = len(x)/2
    
    data = {}

    while(statnum < len(x)):
        if x[statnum].isdigit():
            x[statnum] = int(x[statnum])
        try:
            x[statnum] = float(x[statnum])
        except ValueError:
            pass
        
        data[x[namenum]] = x[statnum]
        namenum += 1
        statnum += 1
        

    return data




if __name__ == "__main__":
    print(zipinfo(sys.argv[1]))
