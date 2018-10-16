##Python 2.7
import re
from datetime import datetime
from operator import itemgetter

## Uses \r\n for DOS and \n for Unix
regex = re.compile(r"\n|\r\n|[\",]")
##unsorted list of objects
objects = []

def main():
    f = raw_input("Enter file name including .csv extension: ")
    with open (f, 'r') as file:
        keys = splitData(file.readline())
        ##handles newline at the end of the first line of the file
        if (keys[-1] == ''):
            keys.pop()
        data = splitData(file.read())
    organizeData(keys, data)
    printSortedData()
    printYears()
    printEntryDate()

##Check if a string is of the datetime format that we are locking for
def validateDate(strDate):
    try:
        datetime.strptime(strDate, '%b %d %Y %I:%M:%S:%f%p')
        return True
    except ValueError:
        return False

##Splits string by commas and returns a list.
##Ignores commas in unclosed double quotes by using regex and delimiter
def splitData(data):
    delimiter = ''
    result = []
    indexes = [-1]    
    for match in regex.finditer(data):
        g = match.group(0)
        if delimiter == '':
            if g in '\r\n,':
                ##adds indexes of all the commas that are not a part of quotes
                indexes.append(match.start())
            elif g in "\"":
                delimiter = g
        elif g == delimiter:
            delimiter = ''
    ## catch unclosed double quotes at the end of the file
    if (delimiter != ''):
        raise ValueError("String is not terminated")
    
    indexes.append(len(data))
    for i in range(len(indexes)-1):
        ##remove doubled quote line separators and whitespaces
        element = data[indexes[i]+1:indexes[i+1]].replace("\n", "").strip()
        if (validateDate(element)):
            ##convert string into datetime object of correct format
            element = datetime.strptime(element, '%b %d %Y %I:%M:%S:%f%p')
        result.append(element)
    return result

##Put data points in a list of dictionary items
def organizeData(keys, data):
    ## handles multiple newline characters at the end of file
    while (len(data)%len(keys) != 0):
        data.pop()
    numData = len(data)
    numKeys = len(keys)
    for i in range(numData/numKeys):
        newDict = {}
        for j in range(numKeys):
            newDict[keys[j]] = data[(numKeys*i)+j]
        objects.append(newDict)

##Print data in sorted or unsorted order depending on if the key exists
def printSortedData():
    sortKeys = ["year","make","model"]
    keyFound = False
    for key in sortKeys:
        if (any(key in obj for obj in objects)):
            keyFound = True
            itemcount = 0
            print "SORTED BY", key.upper(), ":\n---------------------------------------------------------------------------------------------"
            ##Print sorted
            for item in sorted(objects, key=itemgetter(key)):
                itemcount += 1
                printItem(item,itemcount)
    ##Print unsorted
    if (not keyFound):
        print "UNSORTED:\n-----------------------------------------------------------------------------------------------------------",
        itemcount = 0
        for item in objects:
            itemcount += 1
            printItem(item, itemcount)

##Print individual dictionary items in a list
def printItem(data, count):
    print "item number:", count, "\n", data, "\n"

##Print the year of all dictionaries in a list if it exists
def printYears():
    if (any("year" in obj for obj in objects)):
        for obj in objects:
            print "Unsorted year:", obj["year"]
    else:
        print "Year field doesn't exist"

##Printing all Entry dates as datetime objects
def printEntryDate():
    if (any("entrydate" in obj for obj in objects)):
        for obj in objects:
            print "DateTime:", obj["entrydate"], "of Type:", type(obj["entrydate"])
    else:
        print "entrydate field doesn't exist"

##Entry point
if __name__ == "__main__":
    main()
