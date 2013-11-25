

## WE ARE ASSUMING THAT NO TEACHER MAKES LESS THAN $40,000


import urllib2
import requests
import mechanize
import json


SALARY_MIN = 40000

def getSalary(first,last):

    # if last names in spaces (Mr. Brown...)
    last = last.replace(" ","%20")

    if not first:
        url = "http://new-york-employees.findthedata.org/ajax_search?_len=20&page=0&app_id=0&_sortfld=&_sortdir=0&_cnt=-1&_fil[]=lastname%2C%2C%2C%3D%2C"+last+"%2CKV&_zq=&_tpl=srp&head=&dir_field_1="
    else:
        url = "http://new-york-employees.findthedata.org/ajax_search?_len=20&page=0&app_id=0&_sortfld=&_sortdir=0&_cnt=-1&_fil[]=firstname%2C%2C%2C*%2C"+first+"%2CKV&_fil[]=lastname%2C%2C%2C%3D%2C"+last+"%2CKV&_zq=&_tpl=srp&head=&dir_field_1="

    # Give a false user agent to get around permission denied error
    request = urllib2.Request(url, headers={'User-Agent':"Magic Browser"})
    result = urllib2.urlopen(request)

    sal = json.loads(result.read())
    

    salary = []
    for x in sal["data"]:
        if "Department OF Education" in x or "Department of Education" in x:
            salary.append([int(x[2]),x[5]])


    # check only last names in case stuy name != legal name (Mr. brown)
    if len(salary) == 0 and first != None:
        # first replace hyphen with space (Mr. Dyrland-Weaver)
        if "-" in last and "%20" not in last:
            return getSalary(first,last.replace("-","%20"))
        else:
            return getSalary(None,last)


    if not first:
        # if only searching by last name, there must ONLY be one result as to not generate false result
        if len(salary) == 1:
            if salary[0][0] > SALARY_MIN:
                return [salary[0][0],salary[0][1]]
            else:
                return [-1,-1]

    elif len(salary) > 0:     
        for x in salary:
            # check for normal teacher parameters
            if x[0] > SALARY_MIN and x[0] < 110000:
                return [x[0],x[1]]

        if salary[0][0] > SALARY_MIN:
            return [salary[0][0],salary[0][1]]

    return [-1,-1]


if __name__ == "__main__":    
    first = raw_input("First name: ")
    last = raw_input("Last name: ")
    s = getSalary(first,last)
    print("%s %s made $%s in the year %s."%(first,last,s[0],s[1]))
    
