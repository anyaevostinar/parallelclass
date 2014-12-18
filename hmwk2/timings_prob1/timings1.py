import sys
from subprocess import call
common = """
#!/bin/bash -login

#PBS -l walltime=00:01:30
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N parallel1
#PBS -t 1-10

module load NumPy
module load SciPy
module load mpi4py

cd ~/ParallelProc/hmwk2
"""

jobs = ["mpirun -n 1 python sum_reducCol.py 10 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reducCol.py 100 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reducCol.py 5000 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reduc3.py 10 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reduc3.py 100 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reduc3.py 5000 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reduc2.py 10 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reduc2.py 100 1 ${PBS_ARRAYID}",
"mpirun -n 1 python sum_reduc2.py 5000 1 ${PBS_ARRAYID}",]


for job in jobs:
    with open("tmp.sub", 'w') as f:
        f.write(common)
        f.write(job + '\n')

    call(["qsub", 'tmp.sub'])
    call(["rm", 'tmp.sub'])
