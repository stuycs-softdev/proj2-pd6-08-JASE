
import urllib
import requests
import re
from bs4 import BeautifulSoup






posts = [
    '<update mark="" stamp="" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><add name="Document.ActiveSheet" /><set name="Document" add="mode;servercontrol;ie6false" /></update>',
    '<update mark="%s" stamp="%s" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><poll name="17" clearcache="true" /><poll name="5" clearcache="true" /><poll name="9" clearcache="true" /><poll name="8" clearcache="true" /><poll name="16" clearcache="true" /><poll name="15" clearcache="true" /><poll name="14" clearcache="true" /><poll name="13" clearcache="true" /><poll name="12" clearcache="true" /><poll name="11" clearcache="true" /><poll name="10" clearcache="true" /><poll name="7" clearcache="true" /><poll name="6" clearcache="true" /><poll name="4" clearcache="true" /><poll name="3" clearcache="true" /><poll name="Search.DS" clearcache="true" /></update>',
#    '<update mark="%s" stamp="%s" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><set name="17" scrollposition="0:0" /></update>'#,
#    '<update mark="%s" stamp="%s" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><set name="Document.5.Input" search="*zamansky, michael*" /><set name="Document.5.Input" closesearch="accept" /></update>'
    ]



def getSalary(first,last):


    r = requests.post(getURL(),data=posts[0])
    ms = getMarkStamp(r.text)
    for x in range(1,len(posts)):
        k = posts[x]
        da = k%(ms[0],ms[1])
        r = requests.post(getURL(ms[0]),data=k)
        ms = getMarkStamp(r.text)
       
    return r.text


#    r = requests.post(url,data=getData())
#    ms = getMarkStamp(r.text)

 #   tdata = '<update mark="%s" stamp="%s" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><set name="Document.5.Input" search="*zamansky, michael*" /><set name="Document.5.Input" closesearch="accept" /></update>'%(ms[0],ms[1])
#    r = requests.post(url(),data=tdata)

#    ms = getMarkStamp(r.text)
#    tdata = '<update mark="%s" stamp="%s" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><poll name="17" /><poll name="5" /><poll name="8" /><poll name="16" /><poll name="11" /><poll name="7" /><poll name="6" /><poll name="4" /></update>'%(ms[0],ms[1]


 #   return r.text
#    return str(getMarkStamp(r.text))
#    return r.text

def getData(mark="",stamp=""):
    return '<update mark="%s" stamp="%s" cookie="true" scope="Document" view="Clients/Empire Center/Payroll/NY_Payroll_New_York_City.qvw" ident="null"><add name="Document.ActiveSheet" /><set name="Document" add="mode;servercontrol;ie6false" /></update>'%(mark,stamp)

def getMarkStamp(a):
    mark = a.split(' mark="')[1].split('"')[0]
    stamp = a.split(' stamp="')[1].split('"')[0]
    return [mark,stamp]

def getURL(mark=""):
    return "http://qvs.visiblegovernment.us/QvAjaxZfc/QvsViewClient.aspx?mark="+mark+"&host=localhost&view=Clients/Empire%20Center/Payroll/NY_Payroll_New_York_City.qvw&slot=&platform=browser.gecko%2025&dpi=96"
    


if __name__ == "__main__":
    print(getSalary("Mike","Zamansky"))
