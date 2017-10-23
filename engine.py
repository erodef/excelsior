# Engine class
import random
import json
from enum import Enum, auto
from creature import Creature
from components.enemy_ai import Basic
from components.fighter import Fighter
from skill import *
from functions import *
from data_parser import get_monster_data
from room import Room


class Engine():
    """
    Handle game variables and functions.
    """

    title = 'excelsior'
    font = 'fonts/terminal10x16_gs_tc.png'
    altLayout = True
    greyscale = True
    starting = True

    mouse_coordinates = (0, 0)
    screen_width = 80
    screen_height = 45
    bar_width = 20
    panel_height = 15
    panel_y = screen_height - panel_height
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    max_rooms = 30

    first_time = False
    done = False
    dungeon = []
    current_level = Room()

    creature_database = creature_database = get_monster_data(
        'data/monsters.json')

    def gen_dungeon(self, levels):
        for amount in range(levels):
            level = Room(weight=amount)
            candidates = []
            for creature in self.creature_database:
                if creature.weight == level.weight:
                    candidates.append(creature)
            if candidates:
                level.entity = random.choice(candidates)
            self.dungeon.append(level)
            if amount == 0:
                self.current_level = self.dungeon[0]

    def advance(self):
        c = 0
        for level in self.dungeon:
            if self.current_level == level:
                self.current_level = self.dungeon[c+1]
                break
            c += 1
