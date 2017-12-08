# Player class
from entity import Entity


class PC(Entity):
    """
    Player character class
    """
    def __init__(self, name, fighter):
        super().__init__(name, fighter=fighter)
        self.soulstack = 0

    def absorb(self, s):
        self.soulstack += s
