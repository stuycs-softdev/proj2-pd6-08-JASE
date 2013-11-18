import urllib
from bs4 import BeautifulSoup

from pymongo import MongoClient

#Tester
def test():
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-Kevin-Li")
    result = BeautifulSoup(url)
    data = []
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find('span')
        x.find('span').replaceWith(' ');
        if(phoneNum):
            phoneNum = phoneNum.get_text()   
        else:
            phoneNum = 'UnListed PhoneNumber'
        address = x.get_text()
        data.append({"address":address,
                     "phoneNum":phoneNum})
    return data


#Finds the info on someone by using first and last name.
def pFind(first,last):
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-"+ first + "-" +last)
    result = BeautifulSoup(url)
    data = []
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find('span')
        x.find('span').replaceWith(' ');
        if(phoneNum):
            phoneNum = phoneNum.get_text()
        else:
            phoneNum = 'UnListed PhoneNumber'
        address = x.get_text()
        data.append({"address":address,
                 "phoneNum":phoneNum})
    return data

#Puts the information into a database
def AddtoData(first,last):
    d = MongoClient()
    
    person = pFind(first,last)

if __name__ == "__main__":
    first = raw_input("Enter first name: ")
    last = raw_input("Enter last name: ")
    data = pFind(first,last)
    if(list(data) == 0):
        print("This guy doesn't exist")
    else:
        print(pFind(first,last))
