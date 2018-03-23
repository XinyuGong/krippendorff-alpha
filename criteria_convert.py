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
    title = tuple.find(title).text
    min_score = tuple.find(min_score).text
    max_score = tuple.find(max_score).text
    cri[key] = [title, int(min_score), int(max_score)]
SL.save_obj(cri, 'criteria')