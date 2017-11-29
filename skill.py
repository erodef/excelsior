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
    def __init__(self, name, stat, amount, timeout):
        self.name = name
        self.stat = stat
        self.amount = amount
        self.timeout = timeout
        self.icon = self.name[:1]

class Skill:
    def __init__(self, name, timeout, desc, req, actions):
        self.name = name
        self.timeout = timeout
        self.max_timeout = self.timeout
        self.desc = desc
        self.req = req
        self.actions = actions

    def activate(self, user, target):
        results = []
        for action in self.actions:
            results.extend(action.execute(user, target))
        self.timeout = 0
        return results

class Action(ABC):
    def __init__(self, message):
        self.message = message

    @abstractmethod
    def execute(self, user, target):
        pass

class direct_damage(Action):
    def __init__(self, message, dmg):
        super().__init__(message)
        self.dmg = dmg

    def execute(self, user, target):
        results = []

        damage = calculate_damage(user, target, self.dmg)

        kwargs = { 'actor': user.name.capitalize(), 'target': target.name, 'amount': str(damage) }
        if damage > 0:
            results.append({
                'message': Message(self.message.format(**kwargs))
                })

            results.extend(target.take_hit(damage))
        else:
            results.append({'message': Message('{0} tries to attack {1} but the damage is mitigated'.format(user.name.capitalize(), target.name))})

        return results

class guard(Action):
    def __init__(self, message, duration):
        super().__init__(message)
        self.duration = duration

    def execute(self, user, target):
        results = []

        user.buffs.append(Buff('Parry','guard',0 ,self.duration))

        results.append({'message': Message('{0} prepares to parry!'.format(user.name.capitalize()))})

        return results
