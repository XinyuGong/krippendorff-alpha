import SL

irrs = SL.load_obj('irr_prot_i')
new_irrs = dict()
for c_id, irr in irrs.items():
    sum = 0
    max = -99
    for i in irr:
        sum += i
        if i > max: max = i
        #else: print('max:', max, 'i:', i)
    new_irrs[c_id] = max
    if sum / len(irr) > max: print('Impossible scence happens, there must be some bugs...')
    #new_irrs[c_id] = sum / len(irr)
SL.save_obj(new_irrs, 'irr')