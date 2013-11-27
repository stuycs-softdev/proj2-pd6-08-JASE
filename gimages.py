import urllib2
import simplejson


def gImages(teacher):
    data = []
    url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + teacher
    print url
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    results = simplejson.load(response)
    data = results['responseData']
    dataInfo = data['results']
    width = dataInfo['tbWidth']
    height =  dataInfo['tbHeight']
    url = dataInfo['unescapedUrl']
    data.append({"imgWidth":width,
                 "imgHeight":height,
                 "image":url})
    return data
    

if __name__ == "__main__":
    name = raw_input("Name: ")
    print(gImages(name))
