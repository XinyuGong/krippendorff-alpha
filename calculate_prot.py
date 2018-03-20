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
    irr = K.krippendorff_alpha(data = array, metric = K.interval_metric) # interval_metric(default), nominal_metric, ratio_metric
    if irr == -99:
        print('No pairable ratings of any same unit. Give up this criterion.')
        continue
    if c_id in irrs:
        irrs.get(c_id).append(irr)
    else:
        irrs[c_id] = [irr]
    print('is', irr)
SL.save_obj(irrs, 'irr_prot')