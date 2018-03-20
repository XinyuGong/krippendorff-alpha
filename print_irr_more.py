import SL

irrs = SL.load_obj('irr_more')
count = 0
for c_id, tuple in irrs.items():
    count += 1
    print(c_id + ':', tuple[1], '***', tuple[0])
print('Total criteria:', count)