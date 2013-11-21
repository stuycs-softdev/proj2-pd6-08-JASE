
import urllib
import json

def getSalary(first,last):
    url = "http://new-york-employees.findthedata.org/ajax_search?_fil[]=lastname%2C%2C%2C%3D%2C"+last+"%2CKV"
    
    request = urllib.urlopen(url)

    return str(request)


if __name__ == "__main__":
    getSalary("Mike","Zamansky")
    
