from time import time
import sys
from mpi4py import MPI
import math
import numpy as np
import scipy.linalg.blas

def matrix_block_insert(C, c, i, j):
    #assumes square block c                                                     
    c_size = len(c)
    for k in range(c_size):
        C[i+k][j:j+c_size] = c[k]
    return C

def matrix_block_extract(B, block_size, i, j):
    b = []
    for r in range(block_size):
        b.append(B[r+i][j:j+block_size])
    return b

def matrix_mult(a, b, c):
    a_np = np.array(a)
    b_np = np.array(b)
    c_cur = np.array(c)
    c_product = scipy.linalg.blas.dgemm(alpha=1.0, a=a_np.T,trans_a=True, b=b_np.T, trans_b=True)
    c = c_product+c_cur
    return c

N = 6144
p = int(sys.argv[1])
sqrtP = int(math.sqrt(p))
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
part_size = N/sqrtP

A = [range(N)]*N
B = [range(N)]*N
C = []
for i in range(N):
    C.append([0]*N)

myrow = rank/sqrtP
mycol = rank%sqrtP

starttime = MPI.Wtime()
#for submatrix in myrow of A and mycol of B
#mult those two matrices and add to C
i=(myrow*part_size)
j=(mycol*part_size)
for k in range(0, N, part_size):
    a = matrix_block_extract(A, part_size, j, k)
    b = matrix_block_extract(B, part_size, k, i)            
    c = matrix_block_extract(C, part_size, j,i)
    c = matrix_mult(a, b, c)
    C = matrix_block_insert(C, c, j,i)

#reduce the C matrices, adding them together to get complete matrix on 0
C = np.array(C) #np arrays add properly
comm.Barrier()
C = comm.reduce(C, op=MPI.SUM, root=0)
finish=MPI.Wtime()
if rank==0:
    fname = "timing_mult4_"+str(p)+".dat"
    outFile = open(fname, 'w')
    outFile.write(str(finish-starttime))
    outFile.close()
    #print C
