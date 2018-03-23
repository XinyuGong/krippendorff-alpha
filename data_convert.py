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

def process(group, min_score, max_score):
    quant = max_score - min_score + 1
    statical = [[0] * quant] * quant
    for coder, ratings in group.items():
        for unit, score in ratings.items():
            row = score - min_score
            for coder2, ratings2 in group.items():
                if coder2 == coder: continue
                for unit2, score2 in ratings2.items():
                    col = score2 - min_score
                    statical[row][col] += 1
    return statical

def add_up(statical, min_score):
    v_table = {}
    for row in range(len(statical)):
        v_table[row + min_score] = sum(statical[row])
    return v_table

def convert(data, root, site):
    criteria = SL.load_obj('criteria')
    for tuple in root:
        key = tuple.find(t_id).text + '/' + tuple.find(c_id).text # its value is a group of coders' ratings
        coder = tuple.find(ar_id).text
        unit = tuple.find(ae_id).text
        if site == ez:
            s = int(tuple.find(score).text)
        else:
            s = int(tuple.find(rank).text)
        if s < 0:
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
        #min_score = criteria[tuple.find(c_id).text]['min_score']
        #max_score = criteria[tuple.find(c_id).text]['max_score']
        #statical = process(data[key], min_score, max_score)
        #v_table[key] = add_up(statical, min_score)

#import re
#records = open('answers_ez.xml').read()
#records = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",records)
#tree = ET.fromstring(records)
tree = ET.parse('xml/answers_ez_nc.xml')
root = tree.getroot()
data = dict()
#v_table = dict()
convert(data, root, ez)
tree = ET.parse('xml/answers_cv_nc.xml')
root = tree.getroot()
convert(data, root, cv)
SL.save_obj(data, 'data_dict')
#SL.save_obj(v_table, 'v_table')