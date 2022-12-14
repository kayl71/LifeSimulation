import pygame as pg

from Source.Code_source.Creatures import creatures
from Source.Code_source.Managers import genome_manager, food_manager
from Source.Code_source.Visuals import menus, display


class Core:

    def __init__(self):
        """
        Конструктор класса Core.
        """

        self.alive = True   # Существует ли программа
        self.running = False    # Идёт ли симуляция

        pg.init()
        pg.display.set_caption('Life Simulation')

        self.screen_width = 750
        self.screen_height = 750

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

    def start_or_restart(self):
        """
        Создание некоторых атрибутов класса.

        Вынесено в отдельную функцию, так как может понадобиться полный сброс параметров
        этих атрибутов в ходе работы программы, что благодаря этому может быть сделано
        вызовом единственной функции.

        Создаваемые атрибуты:
            camera - объект класса камеры
            fullscreen_menu - объект класса полноэкранного меню
            fs_menu - интерактивное полноэкранное меню
            small_menu - объект класса маленького меню
            open_sm_menu - интерактивное меню, состоящее из одной кнопки открытие маленького меню
            sm_menu - интерактивное маленькое меню, появляющееся во время протекания симуляции
            area_size - размер зоны действий
            food - объект класса FoodManager
            creatures - объект класса CreatureManager
        """

        self.camera = display.Camera(self.screen_width // 2, self.screen_height // 2)

        self.fullscreen_menu = menus.FullScreenMenu(self.screen, self.screen_width, self.screen_height)
        self.fs_menu = self.fullscreen_menu.initialize()
        self.small_menu = menus.SmallMenu(self.screen, self.screen_width, self.screen_height)
        self.open_sm_menu = self.small_menu.open_button()
        self.sm_menu = self.small_menu.initialize()

        while not self.fullscreen_menu.sim_running:
            self.handle_events(pg.event.get(), self.fs_menu, self.open_sm_menu, self.sm_menu)

        self.area_size = self.fullscreen_menu.varset.get_value('area_s')
        food_manager.AreaParameters.AREA_SIZE = self.area_size

        self.food = food_manager.FoodManager(self.fullscreen_menu.varset.get_value('max_food'),
                                             self.fullscreen_menu.varset.get_value('food_speed'),
                                             self.fullscreen_menu.varset.get_value('init_food'))
        self.creatures = genome_manager.CreatureManager(self.fullscreen_menu.varset.get_value('hunt_population'),
                                                        self.fullscreen_menu.varset.get_value('prey_population'))
        creatures.Creature.IS_AGING = self.fullscreen_menu.varset.get_value("aging")

    def run(self):
        """
        Основная функция класса Core, реализующая всю программу.
        """

        self.start_or_restart()
        time_now = pg.time.get_ticks()
        time_last_update = time_now
        UPS = 60  # Update Per Second

        self.food.start(pg.time.get_ticks())

        while self.alive:
            self.handle_events(pg.event.get(), self.fs_menu, self.open_sm_menu, self.sm_menu)
            time_now = pg.time.get_ticks()

            if self.fullscreen_menu.sim_running and time_now - time_last_update > 1000 / UPS:
                self.render()
                self.camera.move(self.screen_width, self.screen_height, self.area_size)
                self.small_menu.run_open_button()
                self.small_menu.run_menu()

                if self.small_menu.sim_running:
                    self.food.update(time_now, time_last_update)
                    self.update((time_now - time_last_update) / 1000)
                time_last_update = time_now

            if not self.small_menu.sim_existing:
                self.running = False
                self.start_or_restart()
                time_last_update = pg.time.get_ticks()
        pg.quit()

    def handle_events(self, events, fs_menu, open_sm_menu, sm_menu):
        """
        Обработчик пользовательских действий

        :param events: события.
        :param fs_menu: полноэкранное меню.
        :param open_sm_menu: кнопка открытия маленького меню.
        :param sm_menu: маленькое меню.
        """

        for event in events:
            if not self.fullscreen_menu.sim_running:
                fs_menu.react(event)
            else:
                if not self.small_menu.running:
                    open_sm_menu.react(event)
                else:
                    sm_menu.react(event)
            if event.type == pg.QUIT:
                self.alive = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.scale_plus()
                elif event.button == 5:
                    self.camera.scale_minus(self.screen_width, self.screen_height, self.area_size)

    def render(self):
        """
        Отрисовка всех объектов на экран
        """
        display.render(self.screen, self.creatures.get(), self.food, self.camera,
                       self.screen_width, self.screen_height, self.area_size)

    def update(self, delta_time):
        """
        Обновляет состояние всех животных на экране

        :param delta_time: отрезок времени, отвечающий за частоту обновления
        """
        self.creatures.update(delta_time, self.food)


if __name__ == "__main__":
    core = Core()
    core.run()
