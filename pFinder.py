import urllib
from bs4 import BeautifulSoup

#Started working on it
#created a pFinder 
#returns the part with address now

url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-Kevin-Li")
result = BeautifulSoup(url)
result = result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'})

def pFind(first,last):
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-%s-%s/0/", first,last).find("li")
    result = BeautifulSoup(url)


print(result);
