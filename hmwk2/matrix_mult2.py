from time import time
import sys

def matrix_mult(a, b, c):
    size = len(a)
    for i in range(size):
        for j in range(size):
            for k in range (size):
                c[i][j] = c[i][j] + (a[i][k] * b[k][j])
    return c

'''
#No longer needed because incorporated into mult
def matrix_add(l, c):
    size = len(l)
    for i in range(size):
        c_cur = c[i]
        c[i] = [x+y for x,y in zip(l[i], c_cur)]
    return c
'''
def matrix_block_insert(C, c, i, j):
    #assumes square block c
    c_size = len(c)
    for k in range(c_size):
        C[i+k][j:j+c_size] = c[k]
    return C

def matrix_block_extract(B, block_size, i, j):
    b = []
    for r in range(block_size):
        b.append(B[r+j][i:i+block_size])
    return b

N = int(sys.argv[1])
block_size = int(sys.argv[2])
A=[]
B=[]
for i in range(N):
    A.append(range(N))
    B.append(range(N))

starttime = time()
#pad with zeros to avoid edges not in blocks
padding = block_size - (N%block_size)
paddedN = N+padding
num_blocks = (paddedN)/block_size

for i in range(padding):
    A.append([0]*N)
    B.append([0]*N)
for i in range(len(A)):
    for j in range(padding):
        A[i].append(0)
        B[i].append(0)

C=[]
#to prevent the rows of C being shallow copies
for i in range(len(A)):
    C.append([0]*len(A))

for i in range(0,paddedN,block_size):
    for j in range(0,paddedN,block_size):
        for k in range(0,paddedN,block_size):
            #print "----------"
            a = matrix_block_extract(A, block_size, k, i)
            #print a, "a"
            b = matrix_block_extract(B, block_size, j, k)
            #print b, 'b'
            c = matrix_block_extract(C, block_size, j, i)
            matrix_mult(a, b,c)
            #print c, 'c'
            C = matrix_block_insert(C, c, i,j)
            #print C

for i in range(padding):
    C = C[0:-1]
for i in range(len(C)):
    for j in range(padding):
        C[i] = C[i][0:-1]

finish = time()

fname = "timing_mult2_"+str(N)+"_"+str(block_size)+".dat"
outFile = open(fname, 'w')
outFile.write(str(finish-starttime))
outFile.close()
'''
for i in range(len(C)):
    print C[i]
'''
