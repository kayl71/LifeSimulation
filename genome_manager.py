import random
import creatures


def make_creature():
    """
    Создаёт новое животное
    :return: экземпляр класса 'Creature'
    """
    return creatures.Creature(size=random.randint(10, 20), speed=random.randint(40, 60), color=(255, 255, 255),
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
    child = creatures.Creature(size, speed, color, x=creature.x, y=creature.y,
                              is_baby=True, energy=creature.energy / 2)
    return child