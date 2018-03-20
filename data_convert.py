import xml.etree.ElementTree as ET
import SL

t_id = 'create_in_task_id'
c_id = 'criterion_id'
ar_id = 'assessor_actor_id'
ae_id = 'assessee_actor_id'
score = 'score'
rank = 'rank'
comm = 'comment'
cv = 'cv'
ez = 'ez'

def convert(data, root, site):
    for tuple in root:
        key = tuple.find(t_id).text + '/' + tuple.find(c_id).text # its value is a group of coders' ratings
        coder = tuple.find(ar_id).text
        unit = tuple.find(ae_id).text
        if site == ez:
            s = tuple.find(score).text
        else:
            s = tuple.find(rank).text
        if int(s) < 0:
            print('tc_id:', key, 'coder:', coder, 'unit:', unit, '* Negative score found. Drop this sample.')
            continue
        if key in data:
            answers = data.get(key)
            if coder in answers:
                answers.get(coder)[unit] = s
            else:
                answers[coder] = {unit: s}
        else:
            data[key] = {coder: {unit: s}}

#import re
#records = open('answers_ez.xml').read()
#records = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",records)
#tree = ET.fromstring(records)
tree = ET.parse('xml/answers_ez_nc.xml')
root = tree.getroot()
data = dict()
convert(data, root, ez)
tree = ET.parse('xml/answers_cv_nc.xml')
root = tree.getroot()
convert(data, root, cv)
SL.save_obj(data, 'data_dict')