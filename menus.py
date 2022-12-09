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


class FullScreenMenu():
    def __init__(self, screen, width, height, running):
        self.screen = screen
        self.width = width
        self.height = height
        self.running = running
        self.alive = True
        self.varset = thorpy.VarSet()

    def run_simulation(self):
        self.running = True
        thorpy.functions.quit_menu_func()

    def initialize(self):
        thorpy.set_theme('human')

        pygame_logo = thorpy.Image('Data_source/Pygame_logo.svg', colorkey=(0,0,0))
        pygame_logo.set_size((180,60))

        thorpy_logo = thorpy.Image('Data_source/Thorpy_logo.png', colorkey=(0, 0, 0))
        thorpy_logo.set_size((80,100))

        pow_by_logos = thorpy.make_group([pygame_logo, thorpy_logo], mode='h')
        pow_by_text = thorpy.make_text('Powered by', font_size=20, font_color=(255,255,255))

        pow_by = thorpy.make_group([pow_by_text, pow_by_logos], mode='v')
        pow_by.set_topleft([self.width-270, self.height - 125])

        team_logo = thorpy.Image('Data_source/Team_logo.png', colorkey=(0, 0, 0))
        team_logo.set_size((180, 95))
        made_by_text = thorpy.make_text("Made by", font_size=27, font_color=(255, 255, 255))

        made_by = thorpy.make_group([made_by_text, team_logo], mode='v')
        made_by.set_topleft([10, self.width - 135])

        bugs = thorpy.Image('Data_source/Bugs.png', colorkey=(0, 0, 0))
        bugs.set_size((600, 300))
        bugs.center()
        bugs.set_topleft((None, 20))
        start_button = thorpy.make_button('Start', func=self.run_simulation)
        start_button.set_size((100,50))
        exit_button = thorpy.make_button('Quit', func=thorpy.functions.quit_func)
        exit_button.set_size((100,50))

        self.varset.add('population', 5, 'Initial population', limits=(1, 500))
        self.varset.add('aging', value=False, text='Aging')
        self.varset.add('max_food', 50, 'Maximal food amount', limits=(20, 10000))
        self.varset.add('food_speed', 1, 'Food generation speed', limits=(0,100))
        self.varset.add('init_food', 50, 'Initial food amount', limits=(20,1000))
        options = thorpy.ParamSetterLauncher.make([self.varset], 'Options', 'Options')
        options.set_size((100,50))

        bg = thorpy.Background(elements=[bugs, made_by, pow_by, start_button,
                                         options, exit_button], color=(100, 100, 100))
        thorpy.store(bg, [start_button, options, exit_button], gap=100, mode='h')
        menu = thorpy.Menu(bg)

        for element in menu.get_population():
            element.surface = self.screen
        menu.play()
        return menu


class SmallMenu(Menu):
    def run_menu(self):
        self.running = True

    def initialize(self):
        thorpy.set_theme('human')

        slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
        button_end = thorpy.make_button("End", func=exit)
        button_pause = thorpy.make_button("Pause", func=exit)
        button_play = thorpy.make_button("Play", func=exit)
        in_timer = thorpy.OneLineText("Days passed")

        box = thorpy.Box(elements=[
            slider,
            button_pause,
            button_play,
            button_end,
            in_timer])
        #reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
        #                            reac_func=slider_reaction,
         #                           event_args={"id": thorpy.constants.EVENT_SLIDE},
          #                          params={},
           #                         reac_name="slider reaction")
        #box.add_reaction(reaction1)

        menu = thorpy.Menu(box)
        for element in menu.get_population():
            element.surface = self.screen

        box.set_topleft((0, 0))
        box.blit()
        box.update()
        return menu, box, in_timer

