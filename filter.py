import SL

criteria = SL.load_obj('irr_more')
result = []
trash = []
for id, tuple in criteria.items():
    rec = [id, tuple[0], tuple[1]]
    result.append(rec)
    '''
    if len(rec[1]) < 40:
        command = input(rec[1] + ' - y or n')
        if command == 'y':
            result.append(rec)
        else:
            trash.append(rec)
    else:
        result.append(rec)
    '''
SL.save_obj(result, 'result')
SL.save_obj(trash, 'trash')