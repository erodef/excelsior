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
from pc import *
from skill import *
from data_parser import *
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

    Game.gen_dungeon(5)

    # Player init
    pskills = [getSkill('punch'), getSkill('kick'), getSkill('scratch')]
    pc_fighter = Fighter(hp=500, sp=100, atk=15, df=10, spd=15, skills=pskills)
    pc = PC('Player', fighter=pc_fighter)

    state = State.ROOM_PHASE

    message_log = MessageLog(Game.message_x, Game.message_width, Game.message_height)

    if Game.starting:
        message_log.add_message(Message('Welcome to Hell'))
        Game.starting = False

    # Draw
    while not tdl.event.is_window_closed():
        con.clear()

        con.draw_str(2, 2, Game.current_level.name)
        con.draw_str(3, 4, Game.current_level.desc)

        if state == State.ROOM_PHASE:
            if Game.current_level.entity:
                con.draw_str(3, 8, "In this room, there is a")
                con.draw_str(28, 8, Game.current_level.entity.name, colors.get('red'))

            # Bottom Panel
            panel_bg = colors.get('lighter_black')
            panel.clear(bg=panel_bg)
            panel.draw_str(2, 2, '[Z] Fight', bg=panel_bg, fg=colors.get('green'))

        elif state == State.BATTLE_PHASE:
            if Game.current_level.entity:
                con.draw_str(3, 8, 'NAME: '+Game.current_level.entity.name.capitalize())
                con.draw_str(3, 10, 'HP: ' +
                            str(Game.current_level.entity.fighter.hp))
                con.draw_str(3, 11, 'SP: '+str(Game.current_level.entity.fighter.sp))

                con.draw_str(3, 12, 'DESC: ' + Game.current_level.entity.desc)


            root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

            # Bottom Panel
            panel_bg = colors.get('lighter_black')
            panel.clear(bg=panel_bg)
            panel.draw_str(2, 2, '[Z] Next Room', bg=panel_bg, fg=colors.get('green'))

        root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)
        root_console.blit(panel, 0, Game.panel_y, Game.screen_width,
                          Game.panel_height, 0, 0)
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
        quit = action.get('quit')
        fullscreen = action.get('fullscreen')
        upgd_menu = action.get('upgd_menu')
        z_press = action.get('z_press')

        # Player movement and controls
        if z_press and state == State.ROOM_PHASE:
            state = State.BATTLE_PHASE

        elif z_press and state == State.BATTLE_PHASE and Game.current_level != Game.dungeon[-1]:
            Game.next_level()
            state = State.ROOM_PHASE

        if quit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if upgd_menu:
            show_upgd_menu = not show_upgd_menu

if __name__ == '__main__':
    main()
