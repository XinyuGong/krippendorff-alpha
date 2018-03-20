import SL

irrs = SL.load_obj('irr')
count = 0
for c_id, irr in irrs.items():
    count += 1
    print(c_id + ':', irr)
print('Total criteria:', count)