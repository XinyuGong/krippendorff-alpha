import SL
import krippendorff_alpha as K

data = SL.load_obj('data_dict')
irrs = dict()
for tc_id, group in data.items():
    c_id = tc_id.split('/')[1]
    array = list()
    for coder, ratings in group.items():
        array.append(ratings)
    print('Calculating IRR for:',tc_id + '...')
    if(len(array) < 3):
        print('Too few answers, give up this criterion.')
        continue
    irr = K.krippendorff_alpha(data = array)
    if irr == -99:
        print('No pairable ratings of any same unit. Give up this criterion.')
        continue
    if c_id in irrs:
        irrs.get(c_id).append(irr)
    else:
        irrs[c_id] = [irr]
SL.save_obj(irrs, 'irr_prot')
new_irrs = dict()
for c_id, irr in irrs.items():
    sum = 0
    for i in irr:
        sum += i
    new_irrs[c_id] = sum / len(irr)
SL.save_obj(new_irrs, 'irr')