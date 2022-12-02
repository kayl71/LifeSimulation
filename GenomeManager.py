import random

import Creature

class Genome:

    def __init__(self):
        pass

    def out(self, distant, direction):
        pass




def CreateCreature():
    return Creature.Creature(random.randint(5, 10), random.randint(1, 5), (255, 255, 255), random.randint(10, 100), random.randint(10, 100))

def CreatePopulation(len : int):
    population = [0]*len
    for i in range(len):
        population[i] = CreateCreature()

    return population

def GetEnergyLoss(size, speed):
    return size * 2 + speed * 1.5