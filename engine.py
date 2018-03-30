# Engine class
import random
import json
import copy
from enum import Enum, auto
from creature import Creature
from pc import PC
from colors import getColors
from game_states import *
from components.enemy_ai import *
from skill import *
from data_parser import get_monster_data, get_skill_data
from room import Room


class Engine:
    class __Engine:
        """
        Handle game variables and functions.
        """

        title = 'excelsior'
        font = 'fonts/cp437_12x12.png'
        altLayout = False
        greyscale = True
        starting = True

        screen_width = 80
        screen_height = 50
        message_x = 4
        message_width = screen_width - 4
        message_height = 7
        mouse = (0, 0)
        mouse_x, mouse_y = mouse
        mousedown = False

        pc_hud_x = int(screen_width/2)-17
        pc_hud_y = screen_height-19

        en_hud_x = int(screen_width/2)-20
        en_hud_y = 5

        combat_locked = False
        gameover = False
        first_time = False
        endtext = ''
        upgd_selec =''
        dungeon_levels = 6
        dungeon = []
        current_level = Room()

        creature_database = get_monster_data('data/monsters.json')
        skill_database = get_skill_data('data/skills.json')
        colors = getColors()

        def __init__(self):
            pskills = [copy.deepcopy(self.skill_database[0]), copy.deepcopy(self.skill_database[1]), copy.deepcopy(self.skill_database[2]), copy.deepcopy(self.skill_database[3])]
            pc_fighter = {'hp':50, 'atk':15, 'df':10, 'spd':15, 'skills':pskills}
            self.__pc = PC('Player', fighter=pc_fighter)

        def gen_dungeon(self, levels):
            self.dungeon = []
            for amount in range(levels):
                level = Room(weight=amount)
                candidates = []
                for creature in self.creature_database:
                    creature.skills = [copy.deepcopy(self.skill_database[0])]
                    if creature.weight <= level.weight:
                        candidates.append(copy.deepcopy(creature))
                if candidates:
                    level.entity = random.choice(candidates)
                self.dungeon.append(level)
                if amount == 0:
                    self.current_level = self.dungeon[0]

        def next_level(self):
            c = 0
            for level in self.dungeon:
                if self.current_level == level:
                    self.current_level = self.dungeon[c+1]
                    break
                c += 1

        def return_player(self):
            return copy.deepcopy(self.__pc)

        def reset(self):
            self.gen_dungeon(self.dungeon_levels)

    instance = None
    def __init__(self):
        if not Engine.instance:
            Engine.instance = Engine.__Engine()
    def __getattr__(self, name):
        return getattr(self.instance, name)
