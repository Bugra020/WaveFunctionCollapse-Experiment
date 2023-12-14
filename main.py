import random
import time
import pygame as pg

TILE_SIZE = 32
ROWS = 20
COLUMNS = 20
WIDTH = TILE_SIZE * COLUMNS
HEIGHT = TILE_SIZE * ROWS
Running = True
isfinished = False

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
IDs = [11, 21, 31, 12, 22, 32, 13, 23, 33, 43, 53, 44, 54, 64]


class Tile(object):
    collapsed = False
    options = IDs
    entropy = len(options)
    pos = (-1, -1)

    def __str__(self):
        return f"{self.collapsed}, {self.entropy}, {self.options}, {self.pos}"


Rules = {
    "11": [[64, 13, 23, 33],
           [12, 13, 54],
           [21, 31, 54],
           [64, 31, 32, 33]],  # 11

    "21": [[64, 13, 23, 33],
           [22, 23, 43, 53],
           [21, 31, 54],
           [11, 21, 44]],  # 12

    "31": [[64, 13, 23, 33],
           [32, 33, 44],
           [64, 11, 12, 13],
           [21, 11, 44]],  # 13

    "12": [[11, 12, 53],
           [12, 13, 54],
           [22, 32, 43, 44],
           [64, 31, 32, 33]],  # 21

    "22": [[21, 44, 54],
           [23, 43, 53],
           [32, 43, 44],
           [12, 53, 54]],  # 22

    "32": [[31, 32, 43],
           [32, 33, 44],
           [11, 12, 13, 64],
           [12, 22, 53, 54]],  # 32

    "13": [[12, 11, 53],
           [64, 11, 21, 31],
           [23, 33, 53],
           [64, 31, 32, 33]],  # 13

    "23": [[21, 22, 44, 54],
           [11, 21, 31, 64],
           [23, 33, 53],
           [23, 13, 43]],  # 23

    "33": [[31, 32, 43],
           [11, 21, 31, 64],
           [11, 12, 13],
           [13, 23, 43]],  # 33

    "43": [[21, 22, 44, 54],
           [32, 33, 44],
           [23, 33, 53],
           [53, 54, 22, 12]],  # 43

    "53": [[44, 54, 21, 22],
           [12, 13, 54],
           [43, 44, 22, 32],
           [13, 23, 43]],  # 53

    "44": [[31, 32, 43],
           [43, 53, 22, 23],
           [21, 31, 54],
           [53, 54, 12, 22]],  # 44

    "54": [[11, 12, 53],
           [43, 53, 22, 23],
           [43, 44, 22, 32],
           [11, 21, 44]],  # 54

    "64": [[13, 23, 33],
           [11, 21, 31],
           [11, 12, 13],
           [31, 32, 33]],  # 64

}

Grids = [Tile] * (ROWS * COLUMNS)

for r in range(0, ROWS):
    for c in range(0, COLUMNS):
        Grids[r * COLUMNS + c] = Tile()
        Grids[r * COLUMNS + c].pos = (r, c)


def wave_function_collapse():
    global ROWS
    global COLUMNS
    global isfinished

    a = 0
    for grid in Grids:
        if grid.collapsed:
            a += 1
    if a == len(Grids):
        isfinished = True

    if not isfinished:

        # low = Tile
        # low.entropy += 1
        index = 0
        for r in range(0, ROWS):
            for c in range(0, COLUMNS):
                if not Grids[r * COLUMNS + c].collapsed:
                    if Grids[r * COLUMNS + c].entropy <= Grids[r * COLUMNS + c - 1].entropy:
                        # low.options = Grids[r * COLUMNS + c].options
                        # low.pos = Grids[r * COLUMNS + c].pos
                        low = Grids[r * COLUMNS + c]
                        index = r * COLUMNS + c

        choice = random.choice(low.options)
        draw_tile(low.pos[0], low.pos[1], choice)
        Grids[index].options = [choice]
        Grids[index].collapsed = True

        for r in range(0, ROWS):
            for c in range(0, COLUMNS):
                if not Grids[r * COLUMNS + c].collapsed:

                    tile = Grids[r * COLUMNS + c]
                    valid = []
                    up = []
                    down = []
                    right = []
                    left = []
                    if tile.pos[0] > 0:
                        neighbor_options = Grids[(r - 1) * COLUMNS + c].options
                        for option in neighbor_options:
                            for i in range(0, len(Rules[f"{option}"][1])):
                                if not Rules[f"{option}"][1][i] in up:
                                    up.append(Rules[f"{option}"][1][i])

                    if tile.pos[1] > 0:
                        neighbor_options = Grids[r * COLUMNS + c - 1].options
                        for option in neighbor_options:
                            for i in range(0, len(Rules[f"{option}"][2])):
                                if not Rules[f"{option}"][2][i] in left:
                                    left.append(Rules[f"{option}"][2][i])

                    if tile.pos[0] < ROWS - 1:
                        neighbor_options = Grids[(r + 1) * COLUMNS + c].options
                        for option in neighbor_options:
                            for i in range(0, len(Rules[f"{option}"][0])):
                                if not Rules[f"{option}"][0][i] in down:
                                    down.append(Rules[f"{option}"][0][i])

                    if tile.pos[1] < COLUMNS - 1:
                        neighbor_options = Grids[r * COLUMNS + c + 1].options
                        for option in neighbor_options:
                            for i in range(0, len(Rules[f"{option}"][3])):
                                if not Rules[f"{option}"][3][i] in right:
                                    right.append(Rules[f"{option}"][3][i])

                    if not up:
                        if not right:
                            valid = list(set(down).intersection(left))
                        elif not left:
                            valid = list(set(down).intersection(right))
                        else:
                            valid = list(set(down).intersection(right, left))
                    elif not down:
                        if not right:
                            valid = list(set(up).intersection(left))
                        elif not left:
                            valid = list(set(up).intersection(right))
                        else:
                            valid = list(set(up).intersection(right, left))
                    elif not right:
                        valid = list(set(up).intersection(down, left))
                    elif not left:
                        valid = list(set(up).intersection(right, down))
                    else:
                        valid = list(set(down).intersection(right, left, up))

                    tile.options = valid


def draw_tile(r, c, id):
    Image = pg.image.load(f"Assets\\tile-{id}.png")
    screen.blit(Image, (c * TILE_SIZE, r * TILE_SIZE))


def main(running):
    while running:
        pg.display.flip()
        wave_function_collapse()
        # time.sleep(.05)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


main(Running)