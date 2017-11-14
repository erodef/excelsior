from logbox import Message


class Skill():
    """
    Skill class
    """
    def __init__(self, name, dmg, blowf, stun, to_hit, cost, timeout, message, atype='direct'):
        self.name = name
        self.attackType = atype
        self.dmg = dmg
        self.cost = cost
        self.timeout = timeout
        self.max_timeout = self.timeout
        self.blowf = blowf
        self.stun = stun
        self.to_hit = to_hit
        self.message = message
        self.requires = []

skilltree = [ Skill('Punch', dmg=10, blowf=1, stun=1, to_hit=70, cost=0, timeout=100, message='{actor} punches {target} dealing {amount} damage!'),

Skill('Kick', dmg=16, blowf=3, stun=3, to_hit=50, cost=5, timeout=100, message='{actor} kicks {target} dealing {amount} damage!'),

Skill('Scratch', dmg=12, blowf=1, stun=1, to_hit=65, timeout=100, cost=1, message='{actor} claws {target} dealing {amount} damage!') ]
