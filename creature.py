import random
from entity import Entity


class Creature(Entity):
    def __init__(self, name, weight, fighter, ai):
        super().__init__(name, fighter=fighter, ai=ai)
        self.weight = weight
