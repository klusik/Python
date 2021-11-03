# no homo

import urllib.request

link = 'http://mathsessions.klusik.cz/?s=semigrupy'
pageObject = urllib.request.urlopen(link)

# content contains byte datatype with all characters on the page
content = pageObject.read()

# make a string out of byte
content = content.decode()

# print(content)

characters = {}

# iterate over string
for i in content:

    if i in characters.keys():
        characters[i] += 1
    else:
        characters[i] = 1
histogram = sorted(characters.items(), key=lambda x: x[1], reverse=True)
print(characters)
print(histogram)