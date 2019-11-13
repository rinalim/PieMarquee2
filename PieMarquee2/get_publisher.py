import xml.etree.ElementTree as ET

print 'Load xml'
doc = ET.parse("/home/pi/png/gamelist_short.xml")
root = doc.getroot()

print 'Lookup data'
def get_publisher(romname):
    filename = romname+".zip"
    publisher = "unknown"
    for item in root:
        if filename in item.findtext('path'):
            publisher = item.findtext('publisher')
            break
    return publisher

print get_publisher('ffight')
