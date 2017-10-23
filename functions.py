import random
from logbox import Message
from game_states import State
from colors import getColors

colors = getColors()

def kill_player(player):
    player.tile = '%'
    player.color = colors.get('dark_red')
    message = Message('You DIED!', colors.get('orange'))

    return message

def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), colors.get('orange'))

    monster.char = '%'
    monster.color = colors.get('dark_red')
    monster.fighter = None
    monster.ai = None
    monster.stopper = False
    monster.name = monster.name + ' corpse'

    return death_message, monster.soulv
