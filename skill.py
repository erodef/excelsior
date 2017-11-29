import random
from abc import ABC, abstractmethod
from logbox import Message

class Buff:
    def __init__(self, name, stat, amount, timeout):
        self.name = name
        self.stat = stat
        self.amount = amount
        self.timeout = timeout

        self.icon = self.name[:1]

class BaseSkill(ABC):
    """
    Abstract class for skills.
    """
    def __init__(self, name, dmg, to_hit, timeout, message):
        self.name = name
        self.desc = ''
        self.dmg = dmg
        self.timeout = timeout
        self.max_timeout = self.timeout
        self.to_hit = to_hit
        self.message = message

    @abstractmethod
    def attack(self, user, target):
        pass

class formula():
    def __init__(self):
        pass

class SkillStdA(BaseSkill):
    """
    Class for standard attack skills. No special effects, just direct damage dealing.
    """
    def __init__(self, name, dmg, to_hit, timeout, message):
        super().__init__(name, dmg, to_hit, timeout, message)

    def attack(self, user, target):
        result = []
        damage = max(0, self.dmg + int(user.atk*0.5) * int(user.spd * 0.3) - target.df + random.randint(-5,+5))

        for buff in target.buffs:
            if buff.stat == 'guard':
                damage = 0

        kwargs = { 'actor': user.name.capitalize(), 'target': target.name, 'amount': str(damage) }
        if damage > 0:
            result.append({
                'message': Message(self.message.format(**kwargs))
                })

            result.extend(target.take_hit(damage))
        else:
            result.append({'message': Message('{0} tries to attack {1} but the damage is mitigated'.format(user.name.capitalize(), target.name))})

        self.timeout = 0
        return result

class SkillScndA(BaseSkill):
    """
    Class for secondary attack skills. Special effects and actions.
    """
    pass

class SkillGd(BaseSkill):
    """
    Class for guard type abillities.
    """
    def __init__(self, name, dmg, to_hit, timeout, message):
        super().__init__(name, dmg, to_hit, timeout, message)

    def attack(self, user, target):
        result = []
        result.append({'message': Message('{0} prepares to parry!'.format(user.name.capitalize()))})
        user.buffs.append(Buff('Parry','guard',0 ,5))

        self.timeout = 0
        return result
