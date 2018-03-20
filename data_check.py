import SL
import sys
import xml.etree.ElementTree as ET

t_id = 'create_in_task_id'
c_id = 'criterion_id'
ar_id = 'assessor_actor_id'
ae_id = 'assessee_actor_id'
score = 'score'
rank = 'rank'
comm = 'comment'
cv = 'cv'
ez = 'ez'
tree = ET.parse('xml/answers_ez_nc.xml')
root = tree.getroot()
data = SL.load_obj('data_dict')
for tuple in root:
        key = tuple.find(t_id).text + '/' + tuple.find(c_id).text # its value is a group of coders' ratings
        coder = tuple.find(ar_id).text
        unit = tuple.find(ae_id).text
        s = tuple.find(score).text
        if int(s) >= 0 and data.get(key).get(coder).get(unit) != s:
            print('Mistake found in', key, 'should be', s, 'but was', data.get(key).get(coder).get(unit))
