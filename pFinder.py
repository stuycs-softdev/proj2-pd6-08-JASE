import urllib
from bs4 import BeautifulSoup


#Tester
def test():
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-Kevin-Li")
    result = BeautifulSoup(url)
    data = []
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find('span')
        tmp = x
        tmp = tmp.find('br')
        tmp.find('span').replaceWith(' ')
        x = x.find('br').replaceWith(' ');
        if(phoneNum):
            phoneNum = phoneNum.get_text()   
        else:
            phoneNum = 'UnListed PhoneNumber'
        address = x.get_text() + tmp.get_text()
        data.append({"address":address,
                     "phoneNum":phoneNum})
    return data


#Finds the info on someone by using first and last name.If not in NY, search NJ
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
    if(len(data) == 0):
        data = pFindNJ(first,last)
    return data

#Finds if person is in NJ, if not returns none found
def pFindNJ(first,last):
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NJ-"+ first + "-" +last)
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
        if(len(data) == 0):
            data.append({"address":"None found",
                         "phoneNum":"None found"})
        return data

if __name__ == "__main__":
    print(test())
    """
    first = raw_input("Enter first name: ")
    last = raw_input("Enter last name: ")
    data = pFind(first,last)
    if(list(data) == 0):
        print("This guy doesn't exist")
    else:
        print(pFind(first,last))
        """
