import json
from creature import Creature
from components.enemy_ai import *
from components.fighter import *
from skill import *


def get_monster_data(path):
    with open (path) as json_data:
        data = json.load(json_data)
        results = []
        for creature in data:
            fighter_c = Fighter(hp=creature["hp"], sp=creature["sp"], atk=creature["atk"], df=creature["df"], spd=creature["spd"])
            ai_c = Basic()

            entry = Creature(creature["name"], creature["weight"], fighter=fighter_c, ai=ai_c)

            entry.desc = creature["desc"]

            results.append(entry)
        return results
