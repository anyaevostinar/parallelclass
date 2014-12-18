from mpi4py import MPI
import numpy as np
import math
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n = int(sys.argv[1])
data = range(int(n))
p = int(sys.argv[2])
id = sys.argv[3]

starttime = MPI.Wtime()
if rank == 0:
    my_sum = 0
    for i in range(n/p):
        my_sum += data[rank+i]
    for i in range(n%p):
        my_sum += data[-(i+1)]
    for i in range(1,p):
        other_sum = comm.recv(source=i)
        my_sum+=other_sum
else:
    my_sum = 0
    for i in range(n/p):
        my_sum +=data[((n/p)*rank)+i]
    comm.send(my_sum, dest=0)

comm.Barrier()
finish = MPI.Wtime()
if rank == 0:
    fname = "timings_reduc2"+str(n)+"_"+str(p)+"_"+id+".dat"
    outFile = open(fname, 'w')
    outFile.write(str(finish-starttime)+"\n")
    outFile.write(str(my_sum))

