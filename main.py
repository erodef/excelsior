# coding=utf-8
"""
    TODO: Progression system
    TODO: Multiple dungeon levels
    TODO: Custom dungeon generation algorithmn
    TODO: Skill Window
    TODO: Combat Revamp
"""
import json
import random
import tdl
import sys
from components.fighter import *
from components.enemy_ai import *
from game_states import *
from engine import *
from input_handlers import *
from rendering import *
from functions import *
from logbox import *
from soul import *
from pc import *
from skill import *
from colors import getColors


def main():

    Game = Engine()
    colors = getColors()

    show_upgd_menu = False

    # TDL init
    tdl.set_font(Game.font, greyscale=Game.greyscale, altLayout=Game.altLayout)
    root_console = tdl.init(Game.screen_width, Game.screen_height, title=Game.title)

    # Gameplay screen
    con = tdl.Console(Game.screen_width, Game.screen_height)

    # UI Panel
    panel = tdl.Console(Game.screen_width, Game.panel_height)

    # Upgrade Screen
    upgd = tdl.Console(Game.screen_width, Game.panel_height)

    # TODO: Change later. GameMap object and Engine Object

    Game.gen_dungeon(5)
    entities = []

    # Player init
    pskills = [getSkill('punch'), getSkill('kick'), getSkill('scratch')]
    pc_fighter = Fighter(hp=500, sp=100, ar=15, df=10, spd=15, skills=pskills)
    pc = PC('Player', fighter=pc_fighter)

    entities.append(pc)

    state = State.PLAYER_TURN

    message_log = MessageLog(Game.message_x, Game.message_width, Game.message_height)
    if Game.starting:
        message_log.add_message(Message('Welcome to Hell'))
        Game.starting = False

    # TODO: Change later. Easy access for entity list
    for entity in Game.dungeon[0].entities:
        entities.append(entity)
        print(entity.tile, entity.name, entity.px, entity.py)

    # Draw
    while not tdl.event.is_window_closed():
        # -------------------------------


        if show_upgd_menu:
            upgd.clear(fg=colors.get('white'), bg=colors.get('black'))
            upgd.draw_str(1, 1, 'Status:')
            upgd.draw_str(10, 1, pc.name)

            upgd.draw_str(1, 6, 'Skills')
            y = 8
            for skill in pc.fighter.skills:
                upgd.draw_str(1, y, ' -'+ skill.name)
                y += 1

            upgd.draw_str(20, 6, 'Souls:')
            upgd.draw_str(28, 6, str(pc.soulstack))

            root_console.blit(upgd, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

        # -------------------------------
        tdl.flush()

        # Clear all entities previous locations. Prevents ghost images
        clear_all(con, entities, pc)

        fov_recompute = False

        # Handle events
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                Game.mouse_coordinates = event.cell

        # If no input matches KEYDOWN, set user_input to None
        else:
            user_input = None

        # If there is no input, continue checking. This means the game only continues if there's user input (Keypress).
        if not user_input:
            continue

        # Input actions

        action = handle_keys(user_input)
        pmove = action.get('pmove')
        quit = action.get('quit')
        fullscreen = action.get('fullscreen')
        upgd_menu = action.get('upgd_menu')

        # Varible to hold results from player turn
        player_turn_results = []

        # Player movement and controls
        if pmove and state == State.PLAYER_TURN and not show_upgd_menu:
            pass

        if quit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if upgd_menu:
            show_upgd_menu = not show_upgd_menu

if __name__ == '__main__':
    main()
