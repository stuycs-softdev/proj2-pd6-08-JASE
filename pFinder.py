import urllib
from bs4 import BeautifulSoup

#Started working on it
#created a pFinder 
#returns the part with address now

url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-Kevin-Li")
result = BeautifulSoup(url)
data = []
for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
    phoneNum = x.find("br", attrs={ 'span class' : 'phoneNumber'})
    if(phoneNum == None):
        phoneNum = 'None'
    else:
        phoneNum = phoneNum.get_text()
    address = x.get_text()
    data.append({"address":address,
                 "phoneNum":phoneNum})


def pFind(first,last):
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-%s-%s/0/", first,last).find("li")
    result = BeautifulSoup(url)
    data = []
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find("br", attrs={ 'span class' : 'phoneNumber'})
        if(phoneNum == None):
            phoneNum = 'None'
        else:
            phoneNum = phoneNum.get_text()
            address = x.get_text()
            data.append({"address":address,
                         "phoneNum":phoneNum})


print(data[0])
