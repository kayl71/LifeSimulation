import time

import pygame as pg
import Display
class Core:

    def __init__(self):
        self.creatures = []
        self.alive = True
        self.running = False
        pg.init()
        width = 800
        height = 800
        self.screen = pg.display.set_mode((width, height))

    def run(self):
        self.start()
        time_now = pg.time.get_ticks()
        time_last_update = time_now
        time_last_render = time_now
        UPS = 4
        FPS = 60

        while self.alive:
            self.handle_events(pg.event.get())

            if self.running and time_now - time_last_update > 1000 / UPS:
                time_last_update = time_now
                self.update()

            if time_now - time_last_render > 1000 / FPS:
                time_last_render = time_now
                self.render()

            time.sleep(1/60)

        pg.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.alive = False

    def render(self):
        Display.render(self.screen)

    def update(self):
        for creature in self.creatures:
            creature.update()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False





if __name__ == "__main__":
    core = Core()
    core.run()