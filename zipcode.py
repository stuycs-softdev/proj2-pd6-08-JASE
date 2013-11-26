import urllib
from bs4 import BeautifulSoup
from operator import itemgetter
import sys

def zipinfo(zipcode):
    url = "http://zipwho.com/?zip=" + zipcode  + "&city=&filters=--_--_--_--&state=&mode=zip"
    page = BeautifulSoup(urllib.urlopen(url))
    x = page.find("script").get_text()
    return x


if __name__ == "__main__":
    print(zipinfo(sys.argv[1]))
