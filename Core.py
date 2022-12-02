import pygame as pg

import Creature
import Display
import FoodManager
import GenomeManager


class Core:

    def __init__(self):
        #self.creatures = GenomeManager.CreatePopulation(1)
        self.creatures = [Creature.Creature(20, 20, (255,255,255), 0, 0)]
        self.food = FoodManager.FoodManager()
        self.alive = True
        self.running = False
        pg.init()
        self.screen_width = 700
        self.screen_height = 700
        self.area_width = 2000
        self.area_height = 2000
        self.camera = Display.Camera(self.screen_width//2, self.screen_height//2)
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))

    def run(self):
        self.start()
        time_now = pg.time.get_ticks()
        time_last_update = time_now
        time_last_fixed_update = time_now
        FUPS = 4  # Fixed Update Per Second
        UPS = 60  # Update Per Second

        while self.alive:
            time_now = pg.time.get_ticks()
            self.handle_events(pg.event.get())

            if self.running and time_now - time_last_fixed_update > 1000 / FUPS:
                time_last_fixed_update = time_now

            if time_now - time_last_update > 1000 / UPS:
                self.update((time_now - time_last_update) / 1000)
                self.render()
                self.camera.move(self.screen_width, self.screen_height, self.area_width, self.area_height)
                self.food.update(time_now)
                time_last_update = time_now

        pg.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.alive = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.scale_plus()
                elif event.button == 5:
                    self.camera.scale_minus(self.screen_width, self.screen_height, self.area_width, self.area_height)

    def fixed_update(self):
        pass

    def render(self):
        Display.render(self.screen, self.creatures, self.food, self.camera, self.screen_width, self.screen_height)

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
