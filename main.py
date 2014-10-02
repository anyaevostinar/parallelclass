import random
import numpy

#Our code yey

class Organism:
  '''A class to contain an organism'''
  def __init__(self, genome=[], parent=False):
    if len(genome):
      self.genome = genome
    elif parent:
      newGenome = parent.genome
      flipBit = random.randint(0, len(newGenome)-1)
      newGenome[flipBit] = 0 if newGenome[flipBit] == 1 else 1
      self.genome = newGenome
    else:
      print "fail"
    self.evalFitness()

  def evalFitness(self):
    self.fitness = 0
    for i in range(len(self.genome)):
      self.fitness += self.genome[i]


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

  def tournamentSelection(self):
    tournamentorgs = set([])
    while len(tournamentorgs)<5:
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
    print fittest.fitness

  def findBest(self, orgs_to_eval=False):
    if not orgs_to_eval:
      orgs_to_eval = self.orgs
    highest_fitness = 0
    for i in range(len(orgs_to_eval)):
      if orgs_to_eval[i].fitness >= highest_fitness:
        highest_fitness = orgs_to_eval[i].fitness
        fittest_org = orgs_to_eval[i]
    return fittest_org

num_updates = 1000
pop_size = 100
population_orgs = Population(pop_size)
for i in range(num_updates):
  population_orgs.update()

print population_orgs.findBest().genome