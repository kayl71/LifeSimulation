import pygame as pg

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
            if self.running and time_now - time_last_update > 1000 / UPS:
                self.update()
            if time_now - time_last_render > 1000 / FPS:
                self.render()




    def render(self):
        pass

    def update(self):
        pass

    def start(self):
        self.running = True

    def stop(self):
        self.running = False





if __name__ == "__main__":
    core = Core()
    core.run()