import random
import Creature


def make_creature():
    """
    Создаёт новое животное

    :return: экземпляр класса 'Creature'
    """
    return Creature.Creature(random.randint(10, 20), random.randint(30, 50), (255, 255, 255),
                             random.randint(-1000, 1000), random.randint(-1000, 1000))


def create_population(length: int):
    """
    Создаёт список заданной длины, состоящий из животных (экземпляров класса 'Creature')

    :param length: количество животных в популяции

    :return: список созданных животных
    """
    population = [make_creature() for _ in range(length)]
    return population


def get_energy_loss(size, speed):
    """
    Рассчитывает потерю энергии животного в зависимости от его размера и скорости

    :param size: размер животного
    :param speed: скорость животного

    :return: количество потерянной энергии
    """
    return (size * 2 + speed * 1.5) / 10
