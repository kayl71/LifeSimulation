import random
import creatures
import food_manager


def make_creature():
    """
    Создаёт новое животное
    :return: экземпляр класса 'Creature'
    """
    type_id_creature = random.randint(0,2)
    if type_id_creature == 0:
        return creatures.Prey(size=random.randint(10, 20), speed=random.randint(40, 60), color=(255, 255, 255),
                             x=random.randint(-1000, 1000), y=random.randint(-1000, 1000))

    return creatures.Hunter(size=random.randint(10, 20), speed=random.randint(40, 60), color=(0, 0, 255),
                             x=random.randint(-1000, 1000), y=random.randint(-1000, 1000))



def create_population(length: int):
    """
    Создаёт список заданной длины, состоящий из животных (экземпляров класса 'Creature')
    :param length: количество животных в популяции
    :return: список созданных животных
    """
    population = [0] * length
    for i in range(length):
        population[i] = make_creature()

    return population


def get_energy_loss(size, speed):
    """
    Рассчитывает потерю энергии животного в зависимости от его размера и скорости
    :param size: размер животного
    :param speed: скорость животного
    :return: количество потерянной энергии
    """
    return (size * 0.9 + speed * 1.7) / 8


def get_child(creature):
    """
    Возвращает потомка животного
    :param creature: животное
    :return: потомок животного
    """
    size = creature.size + random.uniform(-0.5, 0.5)
    speed = creature.speed + random.uniform(-1, 1)
    color = creature.color
    type_creature = type(creature)
    if type_creature is creatures.Hunter:
        child = creatures.Hunter(size, speed, color, x=creature.x, y=creature.y,
                              is_baby=True, energy=creature.energy / 2)
    elif type_creature is creatures.Prey:
        child = creatures.Prey(size, speed, color, x=creature.x, y=creature.y,
                              is_baby=True, energy=creature.energy / 2)
    else:
        child = creatures.Creature(size, speed, color, x=creature.x, y=creature.y,
                              is_baby=True, energy=creature.energy / 2)

    return child

class CreatureManager:

    def __init__(self, start_creatures_count):
        self.creatures = food_manager.Cell()
        creature_list = create_population(start_creatures_count)
        print(creature_list)
        self._replace_creatures(creature_list)

    def update(self, dt, food):
        hunters = []
        for creature_info in self.creatures.get():
            creature = creature_info[2]
            if type(creature) == creatures.Hunter:
                hunters.append(creature)
        for hunter in hunters:
            if hunter.is_dead():
                hunters.remove(hunter)
            else:
                goal = self.creatures.search(hunter.x, hunter.y, True)
                if not goal is None:
                    goal = goal[2]
                hunter.update(dt, goal)
                if hunter.is_reproducing():
                    hunters.append(hunter.get_child())

        preys = []
        for creature_info in self.creatures.get():
            creature = creature_info[2]
            if type(creature) == creatures.Prey and creature.alive:
                preys.append(creature)
        for prey in preys:
            if prey.is_dead():
                preys.remove(prey)
            else:
                prey.update(dt, food)
                if prey.is_reproducing():
                    preys.append(prey.get_child())

        self._replace_creatures(preys+hunters)

    def _replace_creatures(self, creatures):
        self.creatures = food_manager.Cell()
        for creature in creatures:
            self.creatures.add(creature.x, creature.y, creature)

    def get(self):
        creature_list = []
        for creature_info in self.creatures.get():
            creature_list.append(creature_info[2])
        return creature_list