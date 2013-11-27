import urllib
from bs4 import BeautifulSoup


#Tester
def test():
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-Mark-Halperin")
    result = BeautifulSoup(url)
    pridata = []
    data = []
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find('span')
        tmp = x
        #tmp = tmp.find('br')
        tmp.find('span').replaceWith(' ')
        x = x.find('br').replaceWith(' ')
        if(phoneNum):
            phoneNum = phoneNum.get_text()   
        else:
            phoneNum = 'UnListed PhoneNumber'
        address = x.get_text() + tmp.get_text()
        city = x
        city = city.get_text().split(',')[0]
        if("Brooklyn" in city or "New York" in city):
            pridata.append({"address":address,
                         "phoneNum":phoneNum,
                         "test":city})
        else:
            data.append({"address":address,
                         "phoneNum":phoneNum,
                         "test":city})
    data = pridata + data
    return data 


#Finds the info on someone by using first and last name.If not in NY, search NJ
def pFind(first,last):
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NY-"+ first + "-" +last)
    result = BeautifulSoup(url)
    data = []
    pridata =[]
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find('span')
        tmp = x
        #tmp=tmp.find('br')
        tmp.find('span').replaceWith(' ')
        x = x.find('br').replaceWith(' ')
        if(phoneNum):
            phoneNum = phoneNum.get_text()
        else:
            phoneNum = 'UnListed PhoneNumber'
        address = x.get_text() + tmp.get_text()
        city = x
        city = city.get_text().split(',')[0]
        if("Brooklyn" in city or "New York" in city):
            pridata.append({"address":address,
                         "phoneNum":phoneNum,
                         "test":city})
        else:
            data.append({"address":address,
                         "phoneNum":phoneNum,
                         "test":city})
    data = pridata + data
    return data 

#Finds if person is in NJ, if not returns none found
def pFindNJ(first,last):
    url = urllib.urlopen("http://www.peoplefinder.com/people-search/NJ-"+ first + "-" +last)
    result = BeautifulSoup(url)
    data = []
    pridata = []
    for x in result.find_all('div', attrs={'class' : 'ticklerResultsDatum ticklerResultsColAddr datumAddr'}):
        phoneNum = x.find('span')
        tmp = x
        #tmp = tmp.find('br')
        tmp.find('span').replaceWith(' ')
        x = x.find('br').replaceWith(' ')
        if(phoneNum):
            phoneNum = phoneNum.get_text()
        else:
            phoneNum = 'UnListed PhoneNumber'
        address = x.get_text() + tmp.get_text()
        city = x
        city = city.get_text().split(',')[0]
        if("Brooklyn" in city or "New York" in city):
            pridata.append({"address":address,
                         "phoneNum":phoneNum,
                         "test":city})
        else:
            data.append({"address":address,
                         "phoneNum":phoneNum,
                         "test":city})
    data = pridata + data
    return data 

if __name__ == "__main__":
    print(test())

