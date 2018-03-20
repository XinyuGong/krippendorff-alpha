import SL

irrs = SL.load_obj('irr')
criteria = SL.load_obj('criteria')
data = dict()
for id, irr in irrs.items():
    criterion = criteria.get(id)
    if criterion == None:
        print('Criterion not found! ID:', id)
        exit
    list = [criterion, irr]
    data[id] = list
SL.save_obj(data, 'irr_more')