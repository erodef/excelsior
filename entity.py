import math
from copy import deepcopy


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

    def add_skill(self, skill):
        self.skills.append(deepcopy(skill))

    def upgd_skill(self, skill):
        nump = skill.t_name[:1]
        if nump == 'p':
            num = 0
        if nump == 'k':
            num = 1
        if nump == 'g':
            num = 2
        self.skills[num] = deepcopy(skill)

    def change_skill(self, num, skill):
        self.skills[num-1] = deepcopy(skill)

    def take_hit(self, value):
        result = []
        self.hp -= value
        if self.hp <= 0:
            result.append({'dead': self})
        return result
