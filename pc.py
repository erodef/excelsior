# Player class
from entity import Entity


class PC(Entity):
    """
    Player character class
    """
    def __init__(self, name, fighter):
        super().__init__(name, fighter=fighter)
        self.tile = '@'
        # self.soulstack = []
        self.soulstack = 0
        self.render_order = 0

    def absorb(self, s):
        # Add soul to stack
        # self.soulstack.append(s)
        self.soulstack += s

    def enhance(self, weapon):
        # Choose soul -> choose upgrade -> upgrade action
        pass
