from random import shuffle
import numpy as np
from fractions import Fraction

TRIAL = 10000
# frac = Fraction(74126813325120,623360743125120)
# print(frac)


def analyze(v):
    # print(v)
    vecs = np.zeros((5,5))
    for i,c in enumerate(v):
        vecs[i//5][c//5] += 1

    inv = np.transpose(vecs)
    # print(inv)
    top = set()
    for i,x in enumerate(inv):
        max = -1
        ids = []
        for j,c in enumerate(x):
            if j==0:
                max = c
                ids.append(j)
            elif c>max:
                max = c
                ids.clear()
                ids.append(j)
            elif c==max:
                ids.append(j)
        if len(ids) != 1:
            return 0
        top.add(ids[0])
    if len(top)==5:
        # print(vecs)
        return 1
    return 0

aux = 0
for t in range(TRIAL):
    vec = [x for x in range(25)]
    shuffle(vec)
    dx = analyze(vec)
    aux += dx

print(float(aux)/float(TRIAL))