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

m=int(math.log(p, 2))
sent = False
cur_half = p
for i in range(m):
    cur_half=cur_half/2
    if rank >= cur_half and not sent:
        comm.send(my_sum, dest=rank-cur_half)
    if rank < cur_half:
        other_sum = comm.recv(source=rank+cur_half)
        my_sum+=other_sum
comm.Barrier()
finish=MPI.Wtime()
if rank == 0:
    for i in range(n%p):
        my_sum += data[-(i+1)]
    fname = "timings_reduc3"+str(n)+"_"+str(p)+"_"+id+".dat"
    outFile = open(fname, 'w')
    outFile.write(str(finish - starttime)+"\n")
    outFile.write(str(my_sum))

