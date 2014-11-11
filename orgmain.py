import random
import numpy
from mpi4py import MPI

#Our code yey

class Organism:
  '''A class to contain an organism'''
  def __init__(self,pop_x, pop_y, genome=[], parent=False):
    self.age = 0
    self.row_length = pop_x
    self.col_length = pop_y
    self.fitness = 0
    self.rank = comm.Get_rank()

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
      parent.age = 0
    else:
      print "fail"

  def update(self):
    '''Updates the organism's fitness based on its age'''
    self.fitness += self.genome[self.age%len(self.genome)]
    self.age += 1
    if self.fitness >= len(self.genome):
      #reproduce!
      newOrg = Organism(parent=self)
      offspring_genome = numpy.array(newOrg.genome)
      process = determine_cell()
      #comm.Isend(offspring_genome, 
      
  def determine_cell(self):
    #TODO: TEST THIS SHIT
    neighbor = random.randint(0,7)
    process = False

    #Detecting edge cases for toroid
    top_row = False
    bottom_row = False
    left_col = False
    right_col = False
    if self.rank < self.row_length:
      top_row = True
    if self.rank >= (self.row_length * (self.col_length-1)):
      bottom_row = True
    if self.rank%self.row_length == 0:
      left_col = True
    if self.rank%self.row_length == self.row_length -1:
      right_col = True

    if neighbor == 0:
      process = self.rank-self.row_length-1
      if top_row:
        process = process + (self.row_length*self.col_length)
      if left_col:
        process = process + self.row_length
    elif neighbor == 1:
      process = self.rank - self.row_length
      if top_row:
        process = process + (self.row_length*self.col_length)
    elif neighbor == 2:
      process = self.rank - self.row_length +1
      if top_row:
        process = process + (self.row_length*self.col_length)
      if right_col:
        process = process - self.row_length
    elif neighbor == 3:
      process = self.rank -1
      if left_col:
        process = process + self.row_length
    elif neighbor ==4:
      process = self.rank+1
      if right_col:
        process = process - self.row_length
    elif neighbor == 5:
      process = self.rank + self.row_length -1
      if bottom_row:
        process = process - (self.row_length*self.col_length)
      if left_col:
        process = process + self.row_length
    elif neighbor == 6:
      process = self.rank + self.row_length
      if bottom_row:
        process = process - (self.row_length*self.col_length)      
    elif neighbor == 7:
      process = self.rank + self.row_length + 1
      if bottom_row:
        process = process - (self.row_length*self.col_length)
      if right_col:
        process = process - self.row_length

    return process

  def mutate(self):
    newGenome = self.genome
    flipBit = random.randint(0, len(newGenome)-1)
    newGenome[flipBit] = 0 if newGenome[flipBit] == 1 else 1
    self.genome = newGenome
      

class Population:
  '''A class to contain the population and do stuff'''
  def __init__(self, popsize):
    self.currentUpdate = 0
    self.orgs = []
    self.pop_size = popsize
    for i in range(popsize):
      self.orgs.append(self.makeOrg())

  def makeOrg(self):
    '''A function to make a new organism randomly'''
    randomBitArray = numpy.random.randint(2, size=(50,))
    newOrg = Organism(genome=randomBitArray)
    return newOrg

  def update(self):
    '''A function that runs a single update'''
    self.currentUpdate+=1
    current_loc = self.currentUpdate%len(self.orgs[0].genome)
    for org in self.orgs:
      org.update()
      if org.fitness >= len(org.genome):
        newOrg = Organism(parent = org)
        self.orgs.remove(random.choice(self.orgs))
        self.orgs.append(newOrg)

  def findBest(self, orgs_to_eval=False):
    '''Finds the best of the population or a provided subset'''
    if not orgs_to_eval:
      orgs_to_eval = self.orgs
    highest_fitness = 0
    fittest_org = False
    for org in orgs_to_eval:
      if org.fitness > highest_fitness:
        highest_fitness = org.fitness
        fittest_org = org
  
    if not fittest_org:
      print "Error! No Org selected!"
    return fittest_org

  def migrate(self):
    '''Causes all threads to migrate organisms'''
    leaving = random.choice(self.orgs)
    self.orgs.remove(leaving)
    comm.isend(leaving, dest = (rank+1)%size, tag=0)
    arriving = comm.recv(source =(rank+(size-1))%size, tag=0)
    self.orgs.append(arriving)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

num_updates = 1000
pop_x = 10
pop_y = 10
pop_size = pop_x*pop_y
# TODO: when org made by thread, pass in pop_x pop_y
population_orgs = Population(pop_size)
for i in range(num_updates):
  if i%100 == 0:
    population_orgs.migrate()
  population_orgs.update()

best = population_orgs.findBest().genome
data = comm.gather(best, root = 0)

if rank == 0:
  top_fitness = 0
  best_genome = []
  for genome in data:
    temp_fit = sum(genome)
    if top_fitness < temp_fit:
      top_fitness = temp_fit
      best_genome = genome
  print top_fitness
