import thorpy


# ВСЁ МЕНЮ ТРЕБУЕТ ДОРАБОТКИ!!!!


class Menu:
    def __init__(self, screen, width, height, running):
        self.screen = screen
        self.width = width
        self.height = height
        self.running = running
        self.alive = True
        self.varset = thorpy.VarSet()


class FullScreenMenu(Menu):
    def start(self):
        self.running = True
        thorpy.functions.quit_menu_func()

    def initialize(self):
        thorpy.set_theme('human')
        logo = thorpy.Image('Data_source/Logo.png', colorkey=(0, 0, 0))
        logo.set_size((180, 95))
        logo.set_topleft((30, 600))
        bugs = thorpy.Image('Data_source/Bugs.png', colorkey=(0, 0, 0))
        bugs.set_size((600, 300))
        bugs.center()
        bugs.set_topleft((None, 20))
        text = thorpy.make_text("Made by", font_size=30, font_color=(255, 255, 255))
        text.set_topleft((40, 540))
        start_button = thorpy.make_button("Start", func=self.start)
        self.varset.add('population', 5, 'Initial population', limits=(1, 50))
        self.varset.add('aging', value=False, text='Aging')
        self.varset.add('max_food', 50, 'Maximal food amount', limits=(20, 1000))
        options = thorpy.ParamSetterLauncher.make([self.varset], 'Options', 'Params')
        exit_button = thorpy.make_button('Quit', func=thorpy.functions.quit_func)
        bg = thorpy.Background(elements=[bugs, text,
                                         start_button, options, exit_button, logo], color=(100, 100, 100))
        thorpy.store(bg, [start_button, options, exit_button], gap=100, mode='h')
        menu = thorpy.Menu(bg)

        for element in menu.get_population():
            element.surface = self.screen
        menu.play()
        return menu


class SmallMenu(Menu):
    pass
