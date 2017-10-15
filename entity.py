import math
from functions import *


class Entity:
    """
    Entity class for player and creatures
    """
    def __init__(self, name, fighter=None, ai=None):
        self.name = name

        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self
