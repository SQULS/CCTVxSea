from pykml import parser
from lxml import etree
import csv
import sys

path = sys.argv[1]
f = open(path, 'r')
root = parser.parse(f).getroot()
folder = root.Document.Folder
headers = ["name", "latitude", "longitude"]
csvDataObject = []
latitude = ""
longitude = ""
for pm in folder.Placemark:
    name = pm.name.text
    extendeddata = pm.find('.//{http://www.opengis.net/kml/2.2}ExtendedData')
    extendDataArray = []
    for data in extendeddata.findall('.//{http://www.opengis.net/kml/2.2}Data'):
        extendedName = data.get('name')
        if extendedName == "Location":
            location = value = data.find('.//{http://www.opengis.net/kml/2.2}value').text.split(", ")
            latitude = location[0]
            longitude = location[1]
            continue
        value = data.find('.//{http://www.opengis.net/kml/2.2}value').text
        extendDataArray.append(value)
        if extendedName.lower() not in headers:
            headers.append(extendedName.lower())
    compiledDataArray = [name, latitude, longitude]
    compiledDataArray.extend(extendDataArray)
    csvDataObject.append(compiledDataArray)

csvDataObject.insert(0, headers)
with open(sys.argv[2], "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csvDataObject)
