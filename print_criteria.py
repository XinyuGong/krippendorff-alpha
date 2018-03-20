import SL

criteria = SL.load_obj('criteria')
count = 0
for id, title in criteria.items():
    print(id + ': ' + title)
    count += 1
print('Total criteria:', count)