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

            entry.battler = creature["battler"][:1]
            entry.desc = creature["desc"]

            results.append(entry)
        return results

def get_skill_data(path):
    with open (path) as json_data:
        data = json.load(json_data)
        results = []
        for skill in data:
            name, t_name, timeout, desc, rec, actions = skill["name"], skill["t_name"], skill["timeout"], skill["desc"], skill["req"], skill["actions"]
            final_actions = []
            for action in actions:
                new_action = ''
                if action["type"] == "direct_damage":
                    new_action = direct_damage(action["dmg"])

                if action["type"] == "guard":
                    new_action = guard(action["duration"])

                final_actions.append(new_action)
            entry = Skill(name, timeout, desc, rec, final_actions)
            entry.t_name = t_name
            results.append(entry)
        return results
