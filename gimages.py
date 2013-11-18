import urllib

def gImages(teacher):
    url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + teacher
    data = []
	for x in url.find('unescapedUrl'):
		image = x.get_text()
		data.append({"image":image})
	return data


if __name__ == "__main__":
    name = raw_input("Name: ")
    print(gImages(name))
