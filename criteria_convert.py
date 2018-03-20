import xml.etree.ElementTree as ET
import SL

id = 'id'
title = 'title'

tree = ET.parse('xml/criteria.xml')
root = tree.getroot()
cri = dict()
for tuple in root:
    key = tuple.find(id).text
    cri[key] = tuple.find(title).text
SL.save_obj(cri, 'criteria')