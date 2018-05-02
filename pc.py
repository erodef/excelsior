# Player class
from entity import Entity


class PC(Entity):
    """
    Player character class
    """
    def __init__(self, name, fighter):
        super().__init__(name, fighter=fighter)
        self.points = 0

    def level_up_by(self, s):
        self.max_hp += int(self.max_hp*0.2)
        self.hp = self.max_hp
        self.points += s
