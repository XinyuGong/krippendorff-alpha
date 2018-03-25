import SL

irrs = SL.load_obj('irr_more')
count = 0
for c_id, tuple in irrs.items():
    if len(tuple[0]) < 20: continue
    count += 1
    print(c_id + ':', tuple[1], '***', tuple[0])
print('Total criteria:', count)