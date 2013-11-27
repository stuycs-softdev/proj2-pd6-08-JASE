import urllib2
import simplejson

def gImages(first,last):
    url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + first + "%20" + last + "&key=AIzaSyAEH1zvTqgnRGLX8WIerdMnjZiB2Scyys0"

    results = simplejson.load(urllib2.urlopen(urllib2.Request(url)))
    data = results['responseData']
    dataInfo = data['results']
    for myUrl in dataInfo:
        return (myUrl['tbWidth'],myUrl['tbHeight'],myUrl['unescapedUrl'])

if __name__ == "__main__":
    first = raw_input("First Name: ")
    last = raw_input("Last Name: ")
    print(gImages(first,last))
