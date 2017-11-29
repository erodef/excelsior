import math


class Entity:
    """
    Entity class for player and creatures
    """
    def __init__(self, name, fighter, ai=None):
        self.name = name
        self.desc = 'Nothing is know about them.'
        self.battler = "?"

        self.max_hp = fighter.get('hp')
        self.hp = fighter.get('hp')
        self.atk = fighter.get('atk')
        self.df = fighter.get('df')
        self.spd = fighter.get('spd')
        self.skills = fighter.get('skills')

        self.buffs = []

        self.ai = ai

        if self.ai:
            self.ai.owner = self

    def take_hit(self, value):
        result = []
        self.hp -= value
        if self.hp <= 0:
            result.append({'dead': self})
        return result
