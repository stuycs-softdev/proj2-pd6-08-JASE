
import urllib2
import requests
import mechanize
import json

def getSalary(first,last):
    url = "http://new-york-employees.findthedata.org/ajax_search?_len=20&page=0&app_id=0&_sortfld=&_sortdir=0&_cnt=-1&_fil[]=firstname%2C%2C%2C*%2C"+first+"%2CKV&_fil[]=lastname%2C%2C%2C%3D%2C"+last+"%2CKV&_zq=&_tpl=srp&head=&dir_field_1="

    # Give a false user agent to get around permission denied error
    request = urllib2.Request(url, headers={'User-Agent':"Magic Browser"})
    result = urllib2.urlopen(request)

    sal = json.loads(result.read())
    
    try:
        salary = sal["data"][0][2]
        year = sal["data"][0][5]

        return [salary,year]
    except:
        return [-1,-1]


if __name__ == "__main__":    
    first = raw_input("First name: ")
    last = raw_input("Last name: ")
    s = getSalary(first,last)
    print("%s %s made $%s in the year %s."%(first,last,s[0],s[1]))
    
