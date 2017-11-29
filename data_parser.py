import json
from creature import Creature
from components.enemy_ai import *
from skill import *


def get_monster_data(path):
    with open (path) as json_data:
        data = json.load(json_data)
        results = []
        for creature in data:
            fighter_c = {'hp':creature["hp"], 'atk':creature["atk"], 'df':creature["df"], 'spd':creature["spd"]}
            ai_c = Basic()

            entry = Creature(creature["name"], creature["weight"], fighter=fighter_c, ai=ai_c)

            entry.desc = creature["desc"]

            results.append(entry)
        return results

def get_skill_data(path):
    with open (path) as json_data:
        data = json.load(json_data)
        results = []
        for skill in data:
            name, dmg, to_hit, timeout, message = skill["name"], skill["dmg"], skill["to_hit"], skill["timeout"], skill["message"]

            if skill["type"] == 1:
                entry = SkillStdA(name, dmg, to_hit, timeout, message)

            if skill["type"] == 2:
                entry = SkillScdnA(name, dmg, to_hit, timeout, message)

            if skill["type"] == 3:
                entry = SkillGd(name, dmg, to_hit, timeout, message)

            entry.desc = skill["desc"]

            results.append(entry)
        return results
