# Engine class
import random
import json
import copy
from enum import Enum, auto
from creature import Creature
from components.enemy_ai import *
from skill import *
from data_parser import get_monster_data, get_skill_data
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
    screen_height = 40
    message_x = 4
    message_width = screen_width - 4
    message_height = 7
    max_rooms = 30

    bar_width = 30
    pc_hud_x = 4
    pc_hud_y = 5

    en_hud_x = 46
    en_hud_y = 5

    first_time = False
    done = False
    dungeon = []
    current_level = Room()

    creature_database = get_monster_data('data/monsters.json')
    skill_database = get_skill_data('data/skills.json')

    def gen_dungeon(self, levels):
        for amount in range(levels):
            level = Room(weight=amount)
            candidates = []
            for creature in self.creature_database:
                creature.skills = [copy.deepcopy(self.skill_database[0])]
                if creature.weight == level.weight:
                    candidates.append(creature)
            if candidates:
                level.entity = random.choice(candidates)
            self.dungeon.append(level)
            if amount == 0:
                self.current_level = self.dungeon[0]

    def next_stage(self, gamestate):
        if gamestate == State.ROOM_PHASE:
            self.next_level()

    def next_level(self):
        c = 0
        for level in self.dungeon:
            if self.current_level == level:
                self.current_level = self.dungeon[c+1]
                break
            c += 1
