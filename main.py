import random
import numpy
from mpi4py import MPI
import sys

#Our code yey

class Organism:
  '''A class to contain an organism'''
  def __init__(self, genome=[], parent=False):
    if len(genome):
      self.genome = genome
    elif parent:
      newGenome =[]
      for i in range(len(parent.genome)):
        newGenome.append(parent.genome[i])
      flipBit = random.randint(0, len(newGenome)-1)
      newGenome[flipBit] = random.randint(0,1)
      self.genome = newGenome
    else:
      print "fail"
    self.evalFitness()

  def evalFitness(self):
    self.fitness = sum(self.genome)
    return self.fitness


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
    randomBitArray = numpy.random.randint(2, size=(20,))
    newOrg = Organism(genome=randomBitArray)
    return newOrg

  def tournamentSelection(self):
    tournamentorgs = set([])
    while len(tournamentorgs)<3:
      tournamentorgs.add(random.choice(self.orgs))
    tournamentorgs = list(tournamentorgs)
    fittest = self.findBest(tournamentorgs)
    offspring = Organism(parent=fittest)
    self.orgs.remove(tournamentorgs.pop())
    self.orgs.append(offspring)

  def update(self):
    self.currentUpdate+=1
    self.tournamentSelection()
    fittest = self.findBest()

  def findBest(self, orgs_to_eval=False):
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
    leaving = random.choice(self.orgs)
    self.orgs.remove(leaving)
    comm.isend(leaving, dest = (rank+1)%size, tag=0)
    arriving = comm.recv(source =(rank+(size-1))%size, tag=0)
    self.orgs.append(arriving)
    #print "migration!"

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

num_updates = 10000
pop_size = int(sys.argv[1])
starttime = MPI.Wtime()
population_orgs = Population(pop_size)
for i in range(num_updates):
  if i%10 == 0:
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
  #print top_fitness

finish = MPI.Wtime()
if rank == 0:
  fname = "timings_script2.csv"
  outFile = open(fname, 'a')
  outFile.write(str(finish-starttime)+","+str(pop_size)+","+str(size)+","+str(top_fitness)+"\n")
