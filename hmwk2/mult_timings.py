import sys
from subprocess import call
common = """
#!/bin/bash -login

#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N matrix_mult

module load SciPy/0.13.0
module load mpi4py

cd ~/ParallelProc/hmwk2
"""
'''
jobs = ["mpirun -n 1 python matrix_mult1.py 1000",
"mpirun -n 1 python matrix_mult1.py 100",
"mpirun -n 1 python matrix_mult1.py 2000",
"mpirun -n 1 python matrix_mult2.py 1000 16",
"mpirun -n 1 python matrix_mult2.py 100 16",
"mpirun -n 1 python matrix_mult2.py 2000 16",
"mpirun -n 1 python matrix_mult2.py 1000 32",
"mpirun -n 1 python matrix_mult2.py 100 32",
"mpirun -n 1 python matrix_mult2.py 2000 32",
"mpirun -n 1 python matrix_mult2.py 1000 64",
"mpirun -n 1 python matrix_mult2.py 100 64",
"mpirun -n 1 python matrix_mult2.py 2000 64",
"mpirun -n 1 python matrix_mult3.py 100",
"mpirun -n 1 python matrix_mult3.py 2000",
"mpirun -n 1 python matrix_mult3.py 1000"
]
'''
jobs =["mpirun -n 1 python matrix_mult1.py 2000"]
for job in jobs:
    with open("tmp.sub", 'w') as f:
        f.write(common)
        f.write(job + '\n')

    call(["qsub", 'tmp.sub'])
    call(["rm", 'tmp.sub'])
