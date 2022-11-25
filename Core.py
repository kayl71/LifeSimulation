import time

import pygame as pg

import Creature
import Display


class Core:

    def __init__(self):
        self.creatures = [Creature.Prey(color=(255,255,255), direction=100, hunger=0, thurst=0,sleep=0,
                                          koef_take_sun=0,koef_take_plant=0,koef_take_meat=0, size=20, speed=5,
                                          x=100, y=200)]
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
            time_now = pg.time.get_ticks()
            self.handle_events(pg.event.get())

            if self.running and time_now - time_last_update > 1000 / UPS:
                self.update((time_now - time_last_update)/1000)
                time_last_update = time_now

            if time_now - time_last_render > 1000 / FPS:
                self.render()
                time_last_render = time_now

            time.sleep(1/60)

        pg.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.alive = False

    def render(self):
        Display.render(self.screen, self.creatures)

    def update(self, deltaTime):
        for creature in self.creatures:
            creature.update(deltaTime)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False





if __name__ == "__main__":
    core = Core()
    core.run()