import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3.8 or a more recent version is required.")
if sys.version_info[1]<8:
    raise Exception("Python 3.8 or a more recent version is required.")

from math import comb, factorial
import numpy as np
from fractions import Fraction

xsum = comb(25,5)*comb(20,5)*comb(15,5)*comb(10,5)
# print(x)

m5 = [[5,0,0,0,0]]
m4 = [[4,1,0,0,0],[4,0,1,0,0],[4,0,0,1,0],[4,0,0,0,1]]
m3_11 = [[3,1,1,0,0],[3,0,1,1,0],[3,0,0,1,1],[3,1,0,1,0],[3,1,0,0,1],[3,0,1,0,1]]
m3_2 = [[3,2,0,0,0],[3,0,2,0,0],[3,0,0,2,0],[3,0,0,0,2]]
m2_2 = [[2,2,1,0,0],[2,2,0,1,0],[2,2,0,0,1],[2,0,2,1,0],[2,0,0,2,1],[2,0,2,0,1],[2,1,2,0,0],[2,1,0,2,0],[2,1,0,0,2],[2,0,1,2,0],[2,0,1,0,2],[2,0,0,1,2]]
m2_11 = [[2,1,1,1,0],[2,1,1,0,1],[2,1,0,1,1],[2,0,1,1,1]]

bv = m5+m4+m3_11+m3_2+m2_2+m2_11

def place(ss,v,i):
    ss[i] = np.roll(v,i)

def check(ss):
    inv = np.transpose(ss)
    for i in range(5):
        if np.sum(ss[i]) != 5:
            return False
        if np.sum(inv[i]) != 5:
            return False
        twoz = np.where(inv[i] == 2)
        if len(twoz)>1:
            return False
        if len(np.where(inv[i] == 1))>3:
            return False
        if np.argmax(inv[i]) != i:
            # print(ss)
            return False
    return True

def ss_val(ss):
    aux = 1
    cols = [5,5,5,5,5]
    for row in ss:
        # print(row)
        for i,v in enumerate(row):
            aux *= comb(cols[i],v)
            cols[i] -= v
    return aux

aux = 0
seen = set()
for i1,v1 in enumerate(bv):
    print(f"i1 % :{float(i1)/float(len(bv))}")
    for i2,v2 in enumerate(bv):
        # print(f"i2 % :{float(i2)/float(len(bv))}")
        for i3,v3 in enumerate(bv):
            for i4,v4 in enumerate(bv):
                for i5,v5 in enumerate(bv):
                    if (i1,i2,i3,i4,i5) in seen:
                        continue
                   
                    ss = np.zeros((5,5),dtype=int)
                    place(ss,v1,0)
                    place(ss,v2,1)
                    place(ss,v3,2)
                    place(ss,v4,3)
                    place(ss,v5,4)
                    
                    if check(ss):
                        inv = np.transpose(ss)
                        colz = set()
                        for idx in range(5):
                            colz.add(tuple(inv[idx]))
                        colz = frozenset(colz)
                        if colz in seen:
                            continue
                        seen.add(colz)
                        dta = ss_val(ss)
                        # print(f"{ss}:{dta}")
                        aux += dta

css = aux*factorial(5)
print(css)
print(float(css)/float(xsum))
frac = Fraction(css,xsum)
print(frac)