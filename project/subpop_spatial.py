import random
import numpy
from mpi4py import MPI
import sys
import math
random.seed(5)
numpy.random.seed(5)

#Our code yey
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
main_row_len = math.sqrt(size)
main_x = rank%main_row_len
main_y = rank/main_row_len
subpop_size = int(sys.argv[1])

num_updates = 30000
sub_row_length = math.sqrt(subpop_size)
sub_col_length = sub_row_length
total_row_len = sub_row_length*main_row_len
org_length = 20

class Organism:
  '''A class to contain an organism'''
  def __init__(self,index, genome=[], parent=False):
    self.age = 0
    self.fitness = 0
    self.index = index

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

class Subpopulation:
  def __init__(self, subpop_size):
    self.currentUpdate = 0
    self.orgs = []
    self.pop_size = subpop_size
    for i in range(self.pop_size):
      self.orgs.append(Organism(i))

      
  def repro_event(self, org):
    
    neighbor = random.randint(0,7)
    index = org.index
    n_index = False
    top_row = False
    bottom_row = False
    left_col = False
    right_col = False
    if (index < sub_row_length) and (neighbor==0 or neighbor==1 or neighbor==2):
      top_row = True
    if (index >= (sub_row_length * (sub_col_length-1))) and (neighbor==5 or neighbor==6 or neighbor==7):
      bottom_row = True
    if (index%sub_row_length == 0) and (neighbor ==0 or neighbor==3 or neighbor==5):
      left_col = True
    if (index%sub_row_length == sub_row_length -1) and (neighbor==2 or neighbor==4 or neighbor==7):
      right_col = True

    within = not (top_row or bottom_row or left_col or right_col)

    n_index = self.calc_neigh(index, sub_row_length, sub_col_length, neighbor)
    newOrg = Organism(n_index,parent=org)
    if(within):
      self.orgs[n_index] = newOrg

    else:
      rank_neighbor = False
      if top_row and left_col:
        rank_neighbor = 0
      elif top_row and right_col:
        rank_neighbor = 2
      elif bottom_row and left_col:
        rank_neighbor = 5
      elif bottom_row and right_col:
        rank_neighbor = 7
      elif top_row:
        rank_neighbor = 1
      elif left_col:
        rank_neighbor = 3
      elif right_col:
        rank_neighbor = 4
      elif bottom_row:
        rank_neighbor = 6

      n_task = self.calc_neigh(rank, main_row_len, main_row_len, rank_neighbor)
      offspring_genome = numpy.array(newOrg.genome)
      genome_index = numpy.append(offspring_genome, n_index)
      comm.Isend(genome_index, dest=n_task)

  def check_message(self, r,data):
      if(r.Test()):
      #data should have a genome in it
        genome_and_index = data.tolist()
        genome = genome_and_index[:-1]
        index = genome_and_index[-1]
        self.orgs[index] = Organism(index, genome=genome)
      else:
        r.Cancel()


  def update(self):
    '''Runs through an update for the thread'''
  #TODO: put in the possibility of it being empty

    for i in range(len(self.orgs)):
      r_list = []
      data_list = []
      for i in range(7):
        data_list.append(numpy.empty(org_length+1, dtype=numpy.int))
        temp = comm.Irecv(data_list[i], source=MPI.ANY_SOURCE)
        r_list.append(temp)
      self.orgs[i].update()
      if self.orgs[i].fitness >= len(self.orgs[i].genome):
        self.repro_event(self.orgs[i])
      #reproduce!
      for i in range(7):
        self.check_message(r_list[i], data_list[i])
      comm.Barrier()

  def calc_neigh(self, index, row_length, col_length, neighbor):
    top_row = False
    bottom_row = False
    left_col = False
    right_col = False
    if index < row_length:
      top_row = True
    if index >= (row_length * (col_length-1)):
      bottom_row = True
    if index%row_length == 0:
      left_col = True
    if index%row_length == row_length -1:
      right_col = True


    process = False
    if neighbor == 0:
      process = index-row_length-1
      if top_row:
        process = process + (row_length*col_length)
      if left_col:
        process = process + row_length
    elif neighbor == 1:
      process = index - row_length
      if top_row:
        process = process + (row_length*col_length)
    elif neighbor == 2:
      process = index - row_length +1
      if top_row:
        process = process + (row_length*col_length)
      if right_col:
        process = process - row_length
    elif neighbor == 3:
      process = index -1
      if left_col:
        process = process + row_length
    elif neighbor ==4:
      process = index+1
      if right_col:
        process = process - row_length
    elif neighbor == 5:
      process = index + row_length -1
      if bottom_row:
        process = process - (row_length*col_length)
      if left_col:
        process = process + row_length
    elif neighbor == 6:
      process = index + row_length
      if bottom_row:
        process = process - (row_length*col_length)
    elif neighbor == 7:
      process = index + row_length + 1
      if bottom_row:
        process = process - (row_length*col_length)
      if right_col:
        process = process - row_length

    return int(process)

if rank==0:
  starttime=MPI.Wtime()
   
subpop = Subpopulation(subpop_size)

for i in range(num_updates):
  subpop.update()


if rank == 0:
  finish = MPI.Wtime()
  fname = "timings_script5.csv"
  outFile = open(fname, 'a')
  outFile.write(str(finish-starttime)+","+str(subpop_size)+','+str(size)+','+str(subpop_size*size)+'\n')
  outFile.close()
  fname2 = "populations_script5.csv"
  outFile2 = open(fname2, 'a')
  for org in subpop.orgs:
    outFile2.write(str(org.genome)+","+str(subpop_size)+','+str(size)+'\n')

  outFile2.close()
