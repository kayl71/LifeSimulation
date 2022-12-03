import random
import Creature


def CreateCreature():
    return Creature.Creature(random.randint(10, 20), random.randint(30, 50), (255, 255, 255),
                             random.randint(-1000, 1000), random.randint(-1000, 1000))


def CreatePopulation(len: int):
    population = [0] * len
    for i in range(len):
        population[i] = CreateCreature()

    return population


def GetEnergyLoss(size, speed):
    return (size * 2 + speed * 1.5) / 10


def get_child(creature):
    child = Creature.Creature(size=creature.size, speed=creature.speed, color=creature.color, x=creature.x, y=creature.y, is_baby=True,
                              energy=creature.energy/2)
    return child
