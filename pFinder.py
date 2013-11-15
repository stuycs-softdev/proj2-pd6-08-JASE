import urllib
from bs4 import BeautifulSoup

#Started working on it

url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-Mike%20-Zamansky/")
result = BeautifulSoup(url)
l = []


print(result);
