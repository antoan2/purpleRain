# drop #CF12C9
# background #837583

import Tkinter
import time
import math
from Tkinter import Tk
import random
from colour import Color

# size of the window
WIDTH = 800
HEIGHT = 600

DEPTH = 1000 # artificial depth for fake 3d rendering
DT = 0.01
MAX_SPEED = 500 # max speed for the drops
MIN_SPEED = 400 # max speed for the drops
NUM_DROP = 10 # max of new drops each clock

RANDOM_FLASH = 0.99
BACK_DARK = Color("#837583") # background
BACK_LIGHT = Color("#FBF2FB") # backgroud during lightning

purple_dark = Color("#FE00FE") # darkest drops
purple_light = Color("#FFC3FF") # lightest drops
COLORS = list(purple_light.range_to(purple_dark, DEPTH + 1))

class Drop(object):

    # basic particule implementation
    def __init__(self):
        self.y_init = 0
        self.x_init = random.random()*WIDTH
        self.z_init = random.randint(0, DEPTH)
        self.color = COLORS[self.z_init]

        self.y = 0
        self.x = self.x_init
        self.l = 2 + 2*(self.z_init / float(DEPTH))
        self.L = 6 + 5*(self.z_init / float(DEPTH))

        self.speed = MIN_SPEED + (MAX_SPEED - MIN_SPEED) * (3 * self.z_init / float(DEPTH))
        self.dt = DT

    def run(self):
        self.y += self.dt * self.speed

    def __repr__(self):
        return "%s %s" % (self.x, self.y)

class App(object):

    def __init__(self):
        self.root = Tk()

        self.canvas = Tkinter.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.background = self.canvas.create_rectangle(-10,
                                                       -10,
                                                       WIDTH + 10,
                                                       HEIGHT + 10,
                                                       fill=BACK_DARK)

        # to store the drops as (drop, canvas_rectangle)
        self.drops = []
        self.canvas.pack()

        self.root.after(0, self.draw)
        self.root.mainloop()

    def draw(self):
        lightning = False # if we a lightning is on going
        lightning_time = 0 # lightning self time in loop clock
        lightning_duration = 0 # random duration for the lightning

        # main loop
        while True:
            # checks if there is a lightning on going
            if lightning:
                # stop light if too long
                if lightning_time > lightning_duration:
                    self.canvas.itemconfig(self.background, fill=BACK_DARK)
                    lightning_time = 0
                    lightning = False
                else:
                    lightning_time += 1
            # create lightning
            else:
                if random.random() > RANDOM_FLASH:
                    self.canvas.itemconfig(self.background, fill=BACK_LIGHT)
                    lightning_duration = random.randint(5, 10)
                    lightning = True

            # randomizing genrating drops
            # could be done in one loop
            for i in range(random.randint(0, NUM_DROP)):
                drop = Drop()
                rect_drop = self.canvas.create_rectangle(drop.x - drop.l / 2,
                                                                drop.y - drop.L / 2,
                                                                drop.x + drop.l / 2,
                                                                drop.y + drop.L / 2,
                                                                outline='',
                                                                fill=drop.color)
                self.drops.append((drop, rect_drop))

            to_delete = []
            # for each drop, we update pos and speed
            # then we update the corresponding canvas item
            for drop, rect_drop in self.drops:
                drop.run()
                self.canvas.coords(rect_drop,
                                        drop.x - drop.l / 2,
                                        drop.y - drop.L / 2,
                                        drop.x + drop.l / 2,
                                        drop.y + drop.L / 2)
                # if the drop is outside the window we delete it
                if drop.y > HEIGHT + 300:
                    to_delete.append((drop, rect_drop))

            # deleting drops to be deleted
            for drop, rect_drop in to_delete:
                self.canvas.delete(rect_drop)
                self.drops.remove((drop, rect_drop))

            self.canvas.update()
            time.sleep(DT)

            # just in case everything explose
            if len(self.drops) > 1000:
                break

if __name__ == "__main__":
    App()
