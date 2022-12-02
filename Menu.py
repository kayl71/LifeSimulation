import thorpy
import numpy as np


class Menu:
    def __init__(self, screen, width, height, running):
        self.screen = screen
        self.width = width
        self.height = height
        self.running = running


class FullScreenMenu(Menu):
    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def slider_to_real(self, val):
        return np.exp(5 + val)

    def render(self):
        slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
        button_play = thorpy.make_button("Start", func=self.start)
        in_timer = thorpy.OneLineText("Days passed")

        box = thorpy.Box(elements=[
            slider,
            button_play,
            in_timer], size=(800, 800))

        menu = thorpy.Menu(box)
        for element in menu.get_population():
            element.surface = self.screen

        box.set_topleft((0, 0))
        box.blit()
        box.update()
        return menu, box, in_timer


class SmallMenu(Menu):
    pass
