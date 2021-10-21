# Parsing of XML files
#
# In default state the script parses all XML files
# in XML (or ./XML) subfolder and creates a list
# of items with values from that.
#
# It is able to sort things, search the list and so on.

# IMPORTS
import os
import io

# CONFIG

# PATH to XML folder
pathToXMLFolder = "./XMLs"


# Loading the XML files to memory.
#
# XML files are being loaded into the memory and THEN parsed, 
# it's a matter of optimalisation, if the script takes a longer
# time to process the bigger XML files, it could use the link
# to the file for a long time, we don't wanna do that. So better
# option is to load it, save it into memory in bulk and close those 
# files.

def loadXML():

    fileListRaw = os.listdir(pathToXMLFolder)
    fileList = []

    for file in fileListRaw:        
        if file[-4:] == ".xml":
            fileName = pathToXMLFolder+"/"+file
            fileList.append(fileName)
            print(f"{fileName} added to list.")

    print("File list loaded, opening files:")
    xmlData = []
    for file in fileList:
        
        fXml = io.open(file, mode="r", encoding="utf-8")
        print(f"Opening {file}")

        while True:
            xmlLine = fXml.readlines()
            if not xmlLine : break            
            xmlData.append(xmlLine)            
        fXml.close()

    
    print(f"All files successfuly uploaded, read {countOfChars(xmlData)} Bytes.")
    return xmlData

# Characters counter (simply as that)
def countOfChars(list):
    counter = 0
    for item in list:
        for line in item:            
            counter = counter + len(line)
    
    return counter

# Main program (loader)
if __name__ == "__main__":
    # Load XML
    xmlData = loadXML()




