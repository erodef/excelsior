# Engine class
import random
import json
from enum import Enum, auto
from creature import Creature
from generators import gen_words
from room import Room


class Engine():
    """
    Handle game variables and functions.
    """

    title = 'roguevo'
    font = 'terminal12x12_gs_ro.png'
    altLayout = False
    greyscale = True
    starting = True

    mouse_coordinates = (0, 0)
    screen_width = 80
    screen_height = 60
    bar_width = 20
    panel_height = 15
    panel_y = screen_height - panel_height
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    max_rooms = 30

    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 15

    first_time = False
    done = False
    dungeon = []
    current_level = 0

    def gen_dungeon(self, levels):
        for amount in range(levels):
            name = gen_words('world')
            self.dungeon.append(Room(name))
            if amount == 0:
                current_level = self.dungeon[0]

    def move_to(self, t):
        for level in self.dungeon:
            if level.active:
                level.active = False
        t.active = True
        t.populate(12)

    def advance(self):
        c = 0
        for level in self.dungeon:
            if level.active:
                level.active = False
                self.dungeon[c + 1].active = True
                break
            c += 1
