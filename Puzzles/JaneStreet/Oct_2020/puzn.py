from math import comb, factorial
import numpy as np
from fractions import Fraction

N = 5
xsum = 1
tot = N*N
for i in range(N):
    xsum *= comb(tot,N)
    tot -= N
# print(x)

m5 = [[5,0,0,0,0]]
m4 = [[4,1,0,0,0],[4,0,1,0,0],[4,0,0,1,0],[4,0,0,0,1]]
m3_11 = [[3,1,1,0,0],[3,0,1,1,0],[3,0,0,1,1],[3,1,0,1,0],[3,1,0,0,1],[3,0,1,0,1]]
m3_2 = [[3,2,0,0,0],[3,0,2,0,0],[3,0,0,2,0],[3,0,0,0,2]]
m2_2 = [[2,2,1,0,0],[2,2,0,1,0],[2,2,0,0,1],[2,0,2,1,0],[2,0,0,2,1],[2,0,2,0,1],[2,1,2,0,0],[2,1,0,2,0],[2,1,0,0,2],[2,0,1,2,0],[2,0,1,0,2],[2,0,0,1,2]]
m2_11 = [[2,1,1,1,0],[2,1,1,0,1],[2,1,0,1,1],[2,0,1,1,1]]

M = [[3,0,0],[2,1,0],[2,0,1]]
M4 = [[4,0,0,0],[3,1,0,0],[3,0,1,0],[3,0,0,1],[2,2,0,0],[2,0,2,0],[2,0,0,2],[2,1,1,0],[2,1,0,1],[2,0,1,1]]

bv = m5+m4+m3_11+m3_2+m2_2+m2_11

def place(ss,v,i):
    ss[i] = np.roll(v,i)

def check(ss):
    inv = np.transpose(ss)
    for i in range(N):
        if np.sum(ss[i]) != N:
            return False
        if np.sum(inv[i]) != N:
            return False
        if np.argmax(inv[i]) != i:
            # print(ss)
            return False
        mxx = np.max(inv[i])
        if list(inv[i]).count(mxx)>1:
            # print(ss)
            return False
    return True

def ss_val(ss):
    aux = 1
    cols = [N for _ in range(N)]
    for row in ss:
        # print(row)
        for i,v in enumerate(row):
            aux *= comb(cols[i],v)
            cols[i] -= v
    return aux

aux = 0
seen = set()

def flipper(indx,num):
    t0 = 0
    while(t0<(N-1) and indx[t0] == num-1):
        indx[t0] = 0
        t0 += 1
    if t0 == N-1 and indx[t0]==num-1:
        indx[0] = -1
    indx[t0] += 1


indexz = [0 for _ in range(N)]
aux = 0
z = 0
# cases = []
while(True):
    ss = np.zeros((N,N),dtype = int)
    for ti in range(N):
        place(ss,bv[indexz[ti]],ti)

    if check(ss):
        # cases.append([int(x) for x in ss.flatten()])
        dta = ss_val(ss)
        # print(f"{ss}:{dta}")
        aux += dta
        
    z += 1
    flipper(indexz,len(bv))
    if(indexz[0] == -1):
        break

# np.savetxt("c4z.txt",cases,fmt="%d")
# with open("c4.txt","w") as fo:
#     np.savetxt("ct.txt")
print(z) 
css = aux*factorial(N)
print(css)
print(float(css)/float(xsum))
frac = Fraction(css,xsum)
print(frac)
