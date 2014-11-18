import sys
from subprocess import call
common_part1 = """
#!/bin/bash -login

#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn="""
threads = ['1','5','10','1','5','10','100','1','5','10','100','1','5','10','100']
common_part2 = """#PBS -l mem=1gb
#PBS -N maintimings

module load NumPy
module load mpi4py

cd ~/ParallelProc/project/parallelclass
"""

jobs = ["mpirun -n 1 python main.py 100",
"mpirun -n 5 python main.py 20",
"mpirun -n 10 python main.py 10"
"mpirun -n 1 python main.py 300"
"mpirun -n 5 python main.py 60",
"mpirun -n 10 python main.py 30",
"mpirun -n 100 python main.py 3",
"mpirun -n 1 python main.py 500",
"mpirun -n 5 python main.py 100",
"mpirun -n 10 python main.py 50",
"mpirun -n 100 python main.py 5",
"mpirun -n 1 python main.py 1000",
"mpirun -n 5 python main.py 200",
"mpirun -n 10 python main.py 100",
"mpirun -n 100 python main.py 10"
]

for i in range(len(jobs)):
    with open("tmp.sub", 'w') as f:
        f.write(common_part1+threads[i]+"\n"+common_part2)
        f.write(jobs[i] + '\n')

    for i in range(10):
        call(["qsub", 'tmp.sub'])
    call(["rm", 'tmp.sub'])
