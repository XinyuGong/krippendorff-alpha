import SL
import krippendorff_alpha as K

data = SL.load_obj('data_dict')
criteria=SL.load_obj('criteria')
irrs = dict()
for tc_id, group in data.items():
    #if(tc_id!='EZ-00005622/EZ-00005091'): continue
    c_id = tc_id.split('/')[1]
    array = list()
    for coder, ratings in group.items():
        array.append(ratings)
    print('Calculating IRR for:',tc_id + '...')
    if(len(array) < 3):
        print('Too few answers, give up this criterion.')
        continue
    min_ord = criteria[c_id][1]
    ord_quant=criteria[c_id][2]-criteria[c_id][1]+1
    irr = K.krippendorff_alpha(data = array, metric = K.interval_metric, min_ord=min_ord, ord_quant=ord_quant, weighted=True) # interval_metric(default), nominal_metric, ratio_metric, orginal_metric
    if irr == -99:
        print('No pairable ratings of any same unit. Give up this criterion.')
        continue
    if c_id in irrs:
        irrs.get(c_id).append(irr)
    else:
        irrs[c_id] = [irr]
    print('is', irr)
SL.save_obj(irrs, 'irr_prot_i')