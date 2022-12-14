import random
import creatures
import food_manager


class AreaParameters:
    AREA_SIZE = 0


def make_creature(type_id_creature):
    """
    Создаёт новое животное.

    :param type_id_creature: номер типа животного (0 - жертва, 1 - хищник).

    :return: экземпляр соответствующего класса.
    """

    if type_id_creature == 0:
        return creatures.Prey(size=random.randint(10, 20), speed=random.randint(40, 60), color=(255, 255, 255),
                              x=random.randint(-AreaParameters.AREA_SIZE // 2, AreaParameters.AREA_SIZE // 2),
                              y=random.randint(-AreaParameters.AREA_SIZE // 2, AreaParameters.AREA_SIZE // 2))

    elif type_id_creature == 1:
        return creatures.Hunter(size=random.randint(10, 20), speed=random.randint(40, 60), color=(0, 0, 255),
                                x=random.randint(-AreaParameters.AREA_SIZE // 2, AreaParameters.AREA_SIZE // 2),
                                y=random.randint(-AreaParameters.AREA_SIZE // 2, AreaParameters.AREA_SIZE // 2))


def create_population(length: int, cr_type: int):
    """
    Создаёт список заданной длины, состоящий из животных (экземпляров класса 'Creature').

    :param length: количество животных в популяции.
    :param cr_type: тип животного (хищник или жертва).

    :return: список созданных животных.
    """
    population = [make_creature(cr_type) for _ in range(length)]
    return population


def get_energy_loss(size, speed):
    """
    Рассчитывает потерю энергии животного в зависимости от его размера и скорости.

    :param size: размер животного.
    :param speed: скорость животного.

    :return: количество потерянной энергии.
    """
    return (size * 0.9 + speed * 1.7) / 8


def get_child(creature):
    """
    Возвращает потомка животного.

    :param creature: животное.

    :return: потомок животного.
    """

    size = creature.size + random.uniform(-0.5, 0.5)
    speed = creature.speed + random.uniform(-1, 1)
    color = creature.color
    type_creature = type(creature)
    if type_creature is creatures.Hunter:
        child = creatures.Hunter(size, speed, color, x=creature.x, y=creature.y,
                                 is_baby=True, direction=random.randint(0, 359))
    elif type_creature is creatures.Prey:
        child = creatures.Prey(size, speed, color, x=creature.x, y=creature.y,
                               is_baby=True, direction=random.randint(0, 359))
    else:
        child = creatures.Creature(size, speed, color, x=creature.x, y=creature.y,
                                   is_baby=True, direction=random.randint(0, 359))

    return child


class CreatureManager:

    def __init__(self, start_hunters_count, start_preys_count):
        """
        Конструктор класса CreatureManager.

        :param start_hunters_count: начальная популяция хищников.
        :param start_preys_count: начальная популяция жертв.
        """

        self.creatures = food_manager.Cell()
        hunters_list = create_population(start_hunters_count, 1)
        preys_list = create_population(start_preys_count, 0)
        creature_list = hunters_list + preys_list
        self._replace_creatures(creature_list)

    def update(self, dt, food):
        """

        :param dt:
        :param food:

        :return:
        """

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
                hunter.hunter_update(dt, goal)
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
                prey.prey_update(dt, food)
                if prey.is_reproducing():
                    preys.append(prey.get_child())

        self._replace_creatures(preys + hunters)

    def _replace_creatures(self, new_creatures):
        """

        :param new_creatures:

        :return:
        """
        self.creatures = food_manager.Cell()
        for creature in new_creatures:
            self.creatures.add(creature.x, creature.y, creature)

    def get(self):
        """

        :return:
        """
        creature_list = []
        for creature_info in self.creatures.get():
            creature_list.append(creature_info[2])
        return creature_list
