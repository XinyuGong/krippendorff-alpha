#! /usr/bin/env python
# -*- coding: utf-8
'''
Python implementation of Krippendorff's alpha -- inter-rater reliability

(c)2011-17 Thomas Grill (http://grrrr.org)

Python version >= 2.4 required
'''

from __future__ import print_function
try:
    import numpy as np
except ImportError:
    np = None


def nominal_metric(a, b, no_use):
    return a != b


def interval_metric(a, b, no_use):
    return (a-b)**2


def ratio_metric(a, b, no_use):
    return ((a - b) / (a + b)) ** 2 if a > 0 or b > 0 else 0

def ordinal_metric(a, b, v_table):
    if a > b:
        start = int(b)
        end = int(a)
    else:
        start = int(a)
        end = int(b)
    x = 0
    for i in range(start, end + 1):
        x += v_table[i]
    return (x - (v_table[a] + v_table[b]) / 2) ** 2


def krippendorff_alpha(data, metric=interval_metric, force_vecmath=False, convert_items=float, missing_items=None, min_ord = 0, ord_quant = 0, weighted=False):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):
    
    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or 
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items
    
    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    convert_items: function for the type conversion of items (default: float)
    missing_items: indicator for missing items (default: None)
    '''
    
    # number of coders
    #m = len(data)
    
    # set of constants identifying missing values
    if missing_items is None:
        maskitems = []
    else:
        maskitems = list(missing_items)
    if np is not None:
        maskitems.append(np.ma.masked_singleton)
    
    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.items()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)
            
        for it, g in diter:
            x = g[0] if weighted else g #!
            if x not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                y = [convert_items(i) for i in g] if weighted else g #!
                its.append(y)

    units = dict((it, d) for it, d in units.items() if len(d) > 1)  # units with pairable values (delete all units that have ratings less than 1)
    #n = sum(sum(g[1] for g in grades for grades in units.values())) if weighted else sum(len(pv) for pv in units.values())  #! number of pairable values
    
    #np_metric = (np is not None) and ((metric in (interval_metric, nominal_metric, ratio_metric)) or force_vecmath)
    
    #if metric == ordinal_metric:
    statical = []
    for i in range(ord_quant):
        statical.append([0]*ord_quant)
    for grades in units.values():
        l=[]
        d={}
        for grade0 in grades:
            #!
            if weighted:
                grade=grade0[0]
                w=grade0[1]
            else:
                grade=grade0
                w=1
            if grade in d:
                l[d[grade]][1]+=w
            else:
                d[grade]=len(l)
                l.append([grade, w])
            #!
        for i in range(len(l)):
            n = sum(g[1] for g in grades) if weighted else len(grades)
            statical[int(l[i][0])-min_ord][int(l[i][0])-min_ord]+=(l[i][1])*(l[i][1]-1)/(n-1)
            for j in range(i+1, len(l)):
                row = int(l[i][0])-min_ord
                col = int(l[j][0])-min_ord
                statical[row][col]+=l[i][1]*l[j][1]/(n-1)
                statical[col][row]+=l[i][1]*l[j][1]/(n-1)
    v_table = {}
    for row in range(len(statical)):
        v_table[row + min_ord] = sum(statical[row])

    n = sum(v_table.values())
    if n == 0:
        # raise ValueError("No pairable unit's ratings.")
        return -99

    Do = 0.
    for i in range(len(statical) - 1):
        for j in range(i, len(statical)):
            Do += statical[i][j] * metric(i + min_ord, j + min_ord, v_table)
    '''
    for grades in units.values():
        if metric == ordinal_metric:
            Du = sum(metric(gi, gj, v_table, weighted) for gi in grades for gj in grades)
        #elif np_metric:
        #    gr = np.asarray(grades)
        #    Du = sum(np.sum(metric(gr, gri)) for gri in gr)
        else:
            Du = sum(metric(gi, gj, weighted) for gi in grades for gj in grades)
        Do += Du / float(sum(g[1] for g in grades) - 1) if weighted else Du/float(len(grades)-1) #!
    Do /= float(n)
    '''

    if Do == 0:
        return 1.

    De = 0.
    for i in range(len(statical) - 1):
        for j in range(i, len(statical)):
            De += v_table[i + min_ord] * v_table[j + min_ord] * metric(i + min_ord, j + min_ord, v_table)
    De /= (n - 1)
    '''
    for g1 in units.values():
        if metric == ordinal_metric:
            for g2 in units.values():
                De += sum(metric(gi, gj, v_table, weighted) for gi in g1 for gj in g2)
        #elif np_metric:
        #    d1 = np.asarray(g1)
        #    for g2 in units.values():
        #        De += sum(np.sum(metric(d1, gj)) for gj in g2)
        else:
            for g2 in units.values():
                De += sum(metric(gi, gj, weighted) for gi in g1 for gj in g2)
    De /= float(n*(n-1))
    '''

    return 1.-Do/De if (Do and De) else 1.


if __name__ == '__main__': 
    print("Example from http://en.wikipedia.org/wiki/Krippendorff's_Alpha")

    data = (
        "*    *    *    *    *    3    4    1    2    1    1    3    3    *    3", # coder A
        "1    *    2    1    3    3    4    3    *    *    *    *    *    *    *", # coder B
        "*    *    2    1    3    4    4    *    2    1    1    3    3    *    4", # coder C
    )

    missing = '*' # indicator for missing values
    array = [d.split() for d in data]  # convert to 2D list of string items
    print("nominal metric: %.5f" % krippendorff_alpha(array, nominal_metric, missing_items=missing, min_ord = 1, ord_quant=4))
    print("interval metric: %.5f" % krippendorff_alpha(array, interval_metric, missing_items=missing, min_ord = 1, ord_quant=4))
    #print(array)
    array = []
    array.append({'unit6':3, 'unit7':4, 'unit8':1, 'unit9': 2, 'unit10': 1, 'unit11': 1, 'unit12': 3, 'unit13': 3, 'unit15': 3})  # coder 1
    array.append({'unit1':1, 'unit3':2, 'unit4': 1, 'unit5': 3, 'unit6': 3, 'unit7': 4, 'unit8': 3})   # coder 2
    array.append({'unit3':2, 'unit4':1, 'unit5': 3, 'unit6':4, 'unit7':4, 'unit9': 2, 'unit10': 1, 'unit11':1, 'unit12':3, 'unit13':3, 'unit15':4}) # coder 3
    missing = None
    print("ordinal metric: %.5f" % krippendorff_alpha(array, ordinal_metric, missing_items=missing, min_ord = 1, ord_quant=4))
    print("ratio metric: %.5f" % krippendorff_alpha(array, ratio_metric, missing_items=missing, min_ord = 1, ord_quant=4))
