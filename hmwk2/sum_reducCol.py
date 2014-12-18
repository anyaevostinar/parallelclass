from mpi4py import MPI
import numpy as np
import math
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n = int(sys.argv[1])
data = range(n)
p = int(sys.argv[2])
id = sys.argv[3]

starttime=MPI.Wtime()
my_sum =0
for i in range(n/p):
    my_sum+=data[((n/p)*rank)+i]

total = comm.reduce(my_sum, op=MPI.SUM, root=0)

comm.Barrier()
finish=MPI.Wtime()
if rank == 0:
    for i in range(n%p):
        total += data[-(i+1)]
    fname = "timings_reducCol"+str(n)+"_"+str(p)+"_"+id+".dat"
    outFile=open(fname,'w')
    outFile.write(str(finish-starttime)+"\n")
    outFile.write(str(total))

