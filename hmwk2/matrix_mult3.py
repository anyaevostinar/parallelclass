from time import time
import sys
import scipy
import scipy.linalg.blas
import numpy as np

N = int(sys.argv[1])
A= np.ones((1, N))

starttime = time()

C=scipy.linalg.blas.dgemm(alpha=1.0, a=A.T, b=A.T, trans_b=True)

finish = time()

fname = "timing_mult3_"+str(N)+".dat"
outFile = open(fname, 'w')
outFile.write(str(finish-starttime))
outFile.close()

for i in range(len(C)):
    print C[i]

