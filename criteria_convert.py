import xml.etree.ElementTree as ET
import SL

id = 'id'
title = 'title'
min_score = 'min_score'
max_score = 'max_score'

tree = ET.parse('xml/criteria.xml')
root = tree.getroot()
cri = dict()
for tuple in root:
    key = tuple.find(id).text
    text = tuple.find(title).text
    min_s = tuple.find(min_score).text
    max_s = tuple.find(max_score).text
    cri[key] = [text, int(min_s), int(max_s)]
SL.save_obj(cri, 'criteria')