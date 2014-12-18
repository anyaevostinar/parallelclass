import sys
from time import time

N = int(sys.argv[1])
A = [range(N)]*N
B = [range(N)]*N

C=[]
#to prevent the rows of C being shallow copies
for i in range(N):
    C.append([0]*N)

starttime = time()
for i in range(N):
    for j in range(N):
        for k in range (N):
            C[i][j] = C[i][j] + (A[i][k] * B[k][j])

finish= time()
fname = "timing_mult1_"+str(N)+".dat"
outFile = open(fname, 'w')
outFile.write(str(finish-starttime))
outFile.close()

for i in range(N):
    print C[i]

