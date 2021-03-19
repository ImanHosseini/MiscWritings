from random import shuffle
import numpy as np

N = 4
TRIAL = 1000000
cases = np.load("c4.npy")
ctup = []
for c in cases:
    ctup.append(tuple(c.flatten()))
# print(ctup)
nar = np.array([[4,0,0,0],[0,4,0,0],[0,0,4,0],[0,0,0,4]],dtype=int)
# print(np.array_equal(cases[0],nar))
hits = [0 for _ in cases]

def analyze(v):
    # print(v)
    vecs = np.zeros((N,N))
    for i,c in enumerate(v):
        vecs[i//N][c//N] += 1


    inv = np.transpose(vecs)
    # print(inv)
    top = [-1 for _ in range(N)]
    tops = set()
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
        top[i] = ids[0]
        tops.add(ids[0])
    if len(tops) == N:
        # print(vecs)
        mat = np.zeros((N,N),dtype=int)
        for i in range(N):
            mat[i] = vecs[top[i]]
        mat = tuple(mat.flatten())
        # print(ctup)
        wh = [i for i, x in enumerate(ctup) if x == mat]
        if len(wh)!=1:
            print("ERROR")
        # print(wh)
        hits[wh[0]] += 1
        # print("D")
        return 1
    return 0

aux = 0
for t in range(TRIAL):
    vec = [x for x in range(N*N)]
    shuffle(vec)
    dx = analyze(vec)
    aux += dx

print(float(aux)/float(TRIAL))
import pickle
pickle.dump(hits,open("stats.p","wb"))
for i in range(len(hits)):
    if not hits[i]:
        dt = np.array(ctup[i])
        dt = dt.reshape([N,N])
        print(dt)
