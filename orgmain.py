import random
import numpy
from mpi4py import MPI

#Our code yey
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

num_updates = 2000000
row_length = 4
col_length = 4
org_length = 50

assert size == (row_length*col_length), "World size and thread number don't match"

class Organism:
  '''A class to contain an organism'''
  def __init__(self,genome=[], parent=False):
    self.age = 0
    self.fitness = 0

    if len(genome):
      self.genome = genome
    elif parent:
      newGenome =[]
      for i in range(len(parent.genome)):
        newGenome.append(parent.genome[i])
      self.genome = newGenome
      self.mutate()
      parent.mutate()
      parent.fitness = 0
      #parent.age = 0
    else:
      self.genome = numpy.random.randint(2, size=(org_length,)).tolist()

  def update(self):
    '''Updates the organism's fitness based on its age'''
    self.fitness += self.genome[self.age%len(self.genome)]
    self.age += 1
      

  def mutate(self):
    newGenome = self.genome
    flipBit = random.randint(0, len(newGenome)-1)
    newGenome[flipBit] = random.randint(0,1)
    self.genome = newGenome

def determine_cell():
  neighbor = random.randint(0,7)
  process = False

  #Detecting edge cases for toroid
  top_row = False
  bottom_row = False
  left_col = False
  right_col = False
  if rank < row_length:
    top_row = True
  if rank >= (row_length * (col_length-1)):
    bottom_row = True
  if rank%row_length == 0:
    left_col = True
  if rank%row_length == row_length -1:
    right_col = True

  if neighbor == 0:
    process = rank-row_length-1
    if top_row:
      process = process + (row_length*col_length)
    if left_col:
      process = process + row_length
  elif neighbor == 1:
    process = rank - row_length
    if top_row:
      process = process + (row_length*col_length)
  elif neighbor == 2:
    process = rank - row_length +1
    if top_row:
      process = process + (row_length*col_length)
    if right_col:
      process = process - row_length
  elif neighbor == 3:
    process = rank -1
    if left_col:
      process = process + row_length
  elif neighbor ==4:
    process = rank+1
    if right_col:
      process = process - row_length
  elif neighbor == 5:
    process = rank + row_length -1
    if bottom_row:
      process = process - (row_length*col_length)
    if left_col:
      process = process + row_length
  elif neighbor == 6:
    process = rank + row_length
    if bottom_row:
      process = process - (row_length*col_length)      
  elif neighbor == 7:
    process = rank + row_length + 1
    if bottom_row:
      process = process - (row_length*col_length)
    if right_col:
      process = process - row_length

  return process


def update(org):
  '''Runs through an update for the thread'''
  #TODO: put in the possibility of it being empty
  data = numpy.empty(len(org.genome), dtype=numpy.int)
  r = comm.Irecv(data, source=MPI.ANY_SOURCE)
  org.update()
  if org.fitness >= len(org.genome):
      #reproduce!
    newOrg = Organism(parent=org)
    offspring_genome = numpy.array(newOrg.genome)
    process = determine_cell()
    comm.Isend(offspring_genome, dest=process)
  comm.Barrier()
  #test to see if you died
  if(r.Test()):
      #data should have a genome in it
    org = Organism(genome=data.tolist())
  else:
    r.Cancel()
    
  return org
    
org = Organism()

for i in range(num_updates):
  org = update(org)
  #Why does having a barrier here make the threads print more in sync?
  comm.Barrier()
  
for i in range(size):
  if rank ==i:
    fname = "org_test.dat"
    outFile = open(fname, 'a')
    outFile.write(str(org.genome)+"\n")
    comm.Barrier()

print "done"
