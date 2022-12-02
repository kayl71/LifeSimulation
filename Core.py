import time

import pygame as pg

import Creature
import Display
import GenomeManager


class Core:

    def __init__(self):
        self.creatures = GenomeManager.CreatePopulation(5)
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
        time_last_fixed_update = time_now
        FUPS = 4    # Fixed Update Per Second
        UPS = 60    # Update Per Second

        while self.alive:
            time_now = pg.time.get_ticks()
            self.handle_events(pg.event.get())

            if self.running and time_now - time_last_fixed_update > 1000 / FUPS:
                time_last_fixed_update = time_now

            if time_now - time_last_update > 1000 / UPS:
                self.update((time_now - time_last_update)/1000)
                self.render()
                time_last_update = time_now

        pg.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.alive = False

    def fixed_update(self):
        pass

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