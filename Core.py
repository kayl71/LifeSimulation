import pygame as pg

running = False

class Core:

    def __init__(self):
        pg.init()

    def render(self):
        pass

    def update(self):
        pass

    def start(self):
        self.running = True





if __name__ == "__main__":
    core = Core()
    core.start()