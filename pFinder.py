import urllib
from bs4 import BeautifulSoup

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


if __name__ == "__main__":
    first = raw_input("Enter first name: ")
    last = raw_input("Enter last name: ")
    print(pFind(first,last))
