# OOP homo
import urllib.request

class Histogram:
    def __init__(self) -> None:
        self.histogram = {}

    def readWeb(self, url):
        self.pageObject = urllib.request.urlopen(url)

        # content contains byte datatype with all characters on the page
        self.content = self.pageObject.read()

        # make a string out of byte
        self.content = self.content.decode()
        return self.content

    def add(self):
        '''
        method iterate through all characters of the web page
        each character is saved in dict as key
        each new occurance of character is stored as value in the key
        method returns dict
        '''
        # iterate through content of web page
        # content of web page is string data type
        for i in self.content:

            # 
            if i in self.histogram.keys():
                self.histogram[i] += 1
            else:
                self.histogram[i] = 1
        return self.histogram

    def sort(self):
        self.sorted = sorted(self.histogram.items(), key=lambda x: x[1], reverse=True)
        return self.sorted

    def vyblibibli(self):
        print(self.sorted)

hist = Histogram()

hist.readWeb('http://mathsessions.klusik.cz/?s=semigrupy')
hist.add()
hist.sort()
hist.vyblibibli()

print(id(hist))
print(hash(hist))



        