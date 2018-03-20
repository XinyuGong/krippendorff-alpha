import SL

data = SL.load_obj('data_dict')
for tc_id, group in data.items():
    print('tc_id:',tc_id)
    for coder, ratings in group.items():
        print('\tcoder:', coder)
        str = ''
        for unit, score in ratings.items():
            str += unit + ': ' + score + ', '
        print('\t\t' + str)