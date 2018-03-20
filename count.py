import SL

irrs = SL.load_obj('irr_more')
b0 = 0
b2 = 0
b4 = 0
b6 = 0
b8 = 0
b10 = 0
a10 = 0
for id, tuple in irrs.items():
    irr = float(tuple[1])
    if irr < 0:
        b0 += 1
    elif irr < 0.2:
        b2 += 1
    elif irr < 0.4:
        b4 += 1
    elif irr < 0.6:
        b6 += 1
    elif irr < 0.8:
        b8 += 1
    elif irr < 1:
        b10 += 1
    else: a10 += 1
print('< 0:', b0)
print('0 - 0.2:', b2)
print('0.2 - 0.4:', b4)
print('0.4 - 0.6:', b6)
print('0.6 - 0.8:', b8)
print('0.8 - 1.0:', b10)
print('= 1.0:', a10)