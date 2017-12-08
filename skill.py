import random
from abc import ABC, abstractmethod
from logbox import Message


def calculate_damage(user, target, dmg):
    for buff in target.buffs:
        if buff.stat == 'guard':
            return 0
    else:
        return max(0, dmg + int(user.atk*0.5) * int(user.spd * 0.3) - target.df + random.randint(-5,+5))

class Buff:
    def __init__(self, name, stat, value, timeout):
        self.name = name
        self.stat = stat
        self.value = value
        self.timeout = timeout
        self.icon = self.name[:1]

class Skill:
    def __init__(self, name, timeout, desc, req, actions):
        self.name = name
        self.t_name = ''
        self.timeout = timeout
        self.max_timeout = self.timeout
        self.desc = desc
        self.req = req
        self.level = 0
        self.actions = actions

    def upgrade(self):
        for action in self.actions:
            action.upgrade()
        self.level += 1

    def effects(self):
        results = []
        for action in self.actions:
            results.append(action.effect())
        return results

    def activate(self, user, target):
        results = []
        for action in self.actions:
            results.extend(action.execute(user, target))
        self.timeout = 0
        return results

class Action(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self, user, target):
        pass

    @abstractmethod
    def upgrade(self):
        pass

    @abstractmethod
    def effect(self):
        pass

class direct_damage(Action):
    def __init__(self, dmg):
        super().__init__()
        self.dmg = dmg

    def execute(self, user, target):
        results = []
        damage = calculate_damage(user, target, self.dmg)
        if damage > 0:
            results.extend(target.take_hit(damage))
        else:
            pass
        return results

    def upgrade(self):
        self.dmg += int(self.dmg*0.3)

    def effect(self):
        return "Attacks for " +str(self.dmg)+ " damage."

class guard(Action):
    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def execute(self, user, target):
        results = []
        user.buffs.append(Buff('Parry','guard',0 ,self.duration))
        return results

    def upgrade(self):
        self.duration += int(self.duration*0.3)

    def effect(self):
        return "Parries attacks for " +str(self.duration/10)+ " seconds."
