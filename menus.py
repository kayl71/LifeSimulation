import thorpy


class FullScreenMenu:
    def __init__(self, screen, width, height):
        """
        Конструктор класса полноэкранного меню.

        :param screen: экран.
        :param width: ширина экрана.
        :param height: высота экрана.
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.sim_running = False
        self.varset = thorpy.VarSet()

    def reset_params(self):
        """
        Сбрасывает нужные параметры меню
        """
        self.sim_running = False

    def run_simulation(self):
        """
        Выходит из меню и запускает симуляцию.
        """
        self.sim_running = True
        thorpy.functions.quit_menu_func()

    def initialize(self):
        """
        Создаёт полноэкранное меню.

        :return: интерактивное полноэкранное меню.
        """

        thorpy.set_theme('human')

        pygame_logo = thorpy.Image('Data_source/Pygame_logo.svg', colorkey=(0, 0, 0))
        pygame_logo.set_size((18 * self.width / 70, 6 * self.height / 70))

        thorpy_logo = thorpy.Image('Data_source/Thorpy_logo.png', colorkey=(0, 0, 0))
        thorpy_logo.set_size((8 * self.width / 70, self.height / 7))

        pow_by_logos = thorpy.make_group([pygame_logo, thorpy_logo], mode='h')
        pow_by_text = thorpy.make_text('Powered by', font_size=int(20 * (self.height + self.width) / 2 / 700),
                                       font_color=(255, 255, 255))

        pow_by = thorpy.make_group([pow_by_text, pow_by_logos], mode='v')
        pow_by.set_topleft([self.width - 27 * self.width / 70, self.height - 125 * self.height / 700])

        team_logo = thorpy.Image('Data_source/Team_logo.png', colorkey=(0, 0, 0))
        team_logo.set_size((18 * self.width / 70, 95 * self.height / 700))
        made_by_text = thorpy.make_text("Made by", font_size=int(20 * (self.height + self.width) / 2 / 700),
                                        font_color=(255, 255, 255))

        made_by = thorpy.make_group([made_by_text, team_logo], mode='v')
        made_by.set_topleft([10, self.height - 135 * self.height / 700])

        bugs = thorpy.Image('Data_source/Bugs.png', colorkey=(0, 0, 0))
        bugs.set_size((6 * self.width / 7, 3 * self.height / 7))
        bugs.center()
        bugs.set_topleft((None, 2 * self.height / 70))
        start_button = thorpy.make_button('Start', func=self.run_simulation)
        start_button.set_size((self.width / 7, self.height / 14))
        exit_button = thorpy.make_button('Quit', func=thorpy.functions.quit_func)
        exit_button.set_size((self.width / 7, self.height / 14))

        self.varset.add('hunt_population', 5, 'Initial hunters population', limits=(0, 400))
        self.varset.add('prey_population', 5, 'Initial preys population', limits=(0, 400))
        self.varset.add('aging', value=False, text='Aging')
        self.varset.add('max_food', 50, 'Maximal food amount', limits=(20, 10000))
        self.varset.add('food_speed', 1, 'Food generation speed', limits=(0, 400))
        self.varset.add('init_food', 50, 'Initial food amount', limits=(20, 1000))
        self.varset.add('area_s', 2000, 'Area size', limits=(2000, 5000))
        options = thorpy.ParamSetterLauncher.make([self.varset], 'Options', 'Options',
                                                  size=(self.width / 7, self.height / 14))

        bg = thorpy.Background(elements=[bugs, made_by, pow_by, start_button,
                                         options, exit_button], color=(100, 100, 100))
        thorpy.store(bg, [start_button, options, exit_button], gap=self.width / 4, mode='h')
        menu = thorpy.Menu(bg)

        for element in menu.get_population():
            element.surface = self.screen
        menu.play()
        return menu


class SmallMenu:
    def __init__(self, screen, screen_width, screen_height):
        """
        Конструктор класса маленького меню
        :param screen:
        :param screen_width:
        :param screen_height:
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.running = False
        self.sim_running = True
        self.sim_existing = True

    def reset_params(self):
        """
        Сбрасывает нужные параметры меню
        """
        self.running = False
        self.sim_running = True
        self.sim_existing = True

    def start_menu(self):
        """
        Запуск маленького меню.
        """
        self.running = True

    def stop_sim(self):
        """
        Остановка симуляции.
        """
        self.sim_running = False

    def resume(self):
        """
        Возобновление симуляции
        """
        self.sim_running = True
        self.running = False

    def open_fs_menu(self):
        """
        Открытие полноэкранного меню.
        """
        self.sim_existing = False
        self.sim_running = False

    def open_button(self):
        """
        Создание кнопки открытие маленького меню.

        :return: интерактивное меню из одной кнопки.
        """

        options_button = thorpy.make_button('Options', func=self.start_menu)
        self.small_box = thorpy.Box(elements=[options_button])
        menu = thorpy.Menu(self.small_box)
        self.small_box.set_topleft((0, 0))
        for element in menu.get_population():
            element.surface = self.screen
        return menu

    def run_open_button(self):
        """
        Отрисовка и обновление кнопки открытия меню.
        """
        self.small_box.blit()
        self.small_box.update()

    def initialize(self):
        """
        Создание маленького меню.

        :return: интерактивное меню.
        """

        button_end = thorpy.make_button("End", func=self.open_fs_menu)
        button_pause = thorpy.make_button("Pause", func=self.stop_sim)
        button_play = thorpy.make_button("Play", func=self.resume)

        self.box = thorpy.Box(elements=[
            button_pause,
            button_play,
            button_end], size=(80 * self.screen_width / 700, 100 * self.screen_height / 700))
        self.box.set_topleft((0, 0))
        menu = thorpy.Menu(self.box)
        for element in menu.get_population():
            element.surface = self.screen
        return menu

    def run_menu(self):
        """
        Отрисовка и обновление маленького меню.
        """
        if self.running:
            self.box.blit()
            self.box.update()
