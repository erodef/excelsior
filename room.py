import random
from creature import Creature
from components.fighter import *
from components.enemy_ai import *
from skill import *


class Room:
    """
    Dungeon level class
    """
    ID = 0
    def __init__(self, name='Empty Room', weight=0, creature=None):
        Room.ID += 1
        self.id = Room.ID
        self.name = name.capitalize()
        self.weight = weight
        self.desc = 'An empty room. Vast, dark and filled with dust.'
        self.entity = creature
