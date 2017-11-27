from abc import ABC, abstractmethod
from logbox import Message


class BaseSkill(ABC):
    """
    Abstract class for skills.
    """
    def __init__(self, name, dmg, to_hit, cost, timeout, message):
        self.name = name
        self.dmg = dmg
        self.cost = cost
        self.timeout = timeout
        self.max_timeout = self.timeout
        self.to_hit = to_hit
        self.message = message

    @abstractmethod
    def attack(self, user, target):
        pass

class SkillStdA(BaseSkill):
    def __init__(self, name, dmg, to_hit, cost, timeout, message):
        super().__init__(name, dmg, to_hit, cost, timeout, message)

    def attack(self, user, target):
        pass

class SkillGd(BaseSkill):
    def __init__(self, name, dmg, to_hit, cost, timeout, message):
        super().__init__(name, dmg, to_hit, cost, timeout, message)

    def attack(self, user, target):
        pass

skillpunch = SkillStdA('Punch', dmg=10, to_hit=70, cost=0, timeout=100, message='{actor} punches {target} dealing {amount} damage!')

skillguard = SkillGd('Parry', dmg=0, to_hit=100, timeout=50, cost=1, message='{actor} prepares to parry!')
