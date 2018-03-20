import SL

irrs = SL.load_obj('irr_prot')
new_irrs = dict()
'''
for c_id, irr in irrs.items():
    sum = 0
    for i in irr:
        sum += i
    new_irrs[c_id] = sum / len(irr)
'''
for c_id, irr in irrs.items():
    max = irr[0]
    for i in irr:
        if i > max:
            max = i
    new_irrs[c_id] = max
SL.save_obj(new_irrs, 'irr')