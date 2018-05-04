# coding=utf-8
"""
    TODO: -EXTRA- Battle visuals (hit numbers, hit marks, warnings, different monster sprites etc)
    TODO: -EXTRA- Choices during dungeon movement
"""
import json
import random
import tdl
import sys
import copy
from components.enemy_ai import *
from engine_combat import *
from engine import *
from rendering import *
from logbox import *
from pc import *
from skill import *
from data_parser import *
from colors import getColors


def main():
    G = Engine()
    colors = G.colors
    mact_counter = 0
    menu_cursor = 0

    # TDL init
    tdl.set_font(G.font, greyscale=G.greyscale, altLayout=G.altLayout)
    root_console = tdl.init(G.screen_width, G.screen_height, title=G.title)
    tdl.set_fps(30)

    # Console
    con = tdl.Console(G.screen_width, G.screen_height)

    # Player init
    pc = G.return_player()

    if not G.started:
        G.state = State.MENU
        G.gen_dungeon(G.dungeon_levels)
        G.started = True

    # Draw
    while not tdl.event.is_window_closed():
        con.clear()

        # Drawing on screen in menu
        if G.state == State.MENU:
            draw_menu(con, G)
            text = "teste teste [1, 2, 3]{} mais uma [véz]."
            print(draw_colored_line(con, 2, 3, text))

        # Drawing on screen in room
        if G.state == State.ROOM_PHASE:
            draw_room(con, G)

        # Drawing on screen during battle
        if G.state == State.BATTLE_PHASE:
            draw_battle(con, G, pc)
            root_console.blit(con, 0, 0, G.screen_width, G.screen_height, 0, 0)

        # Drawing on screen after battle
        if G.state == State.UPGD_PHASE:
            draw_upgd(con, G, pc)

        # Drawing on screen on game ending phase
        if G.state == State.ENDING:
            draw_ending(con, G)

        root_console.blit(con, 0, 0, G.screen_width, G.screen_height, 0, 0)
        tdl.flush()

        # Handle events
        G.mousedown = False
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                G.mouse = event.cell
                G.mouse_x, G.mouse_y = G.mouse
            if event.type == 'MOUSEDOWN':
                G.mousedown = True
        # If no input matches KEYDOWN, set user_input to None
        else:
            user_input = None

        # Handling events in different G.states
        if G.state == State.BATTLE_PHASE:
            enemy = G.current_level.entity
            results = []

            if G.combat_locked:
                # Player
                for skill in pc.skills:
                    if skill.timeout < skill.max_timeout:
                        skill.timeout += 1

                for buff in pc.buffs:
                    if buff.timeout > 0:
                        buff.timeout -= 1
                    else:
                        del pc.buffs[pc.buffs.index(buff)]

                # Handles user attack inputs
                if user_input:
                    if user_input.keychar == '1' or user_input.keychar == '2' or user_input.keychar == '3' or user_input.keychar == '4':
                        skill = pc.skills[int(user_input.keychar) - 1]
                        if skill.timeout == skill.max_timeout:
                            results = skill.activate(pc, enemy)

                # Enemy
                for skill in enemy.skills:
                    if skill.timeout < skill.max_timeout:
                        skill.timeout += 1

                for buff in enemy.buffs:
                    if buff.timeout > 0:
                        buff.timeout -= 1
                    else:
                        del enemy.buffs[enemy.buffs.index(buff)]

                # Making the enemy attack
                if mact_counter < 50:
                    mact_counter += 1
                else:
                    skill = random.choice(enemy.skills)
                    if skill.timeout >= skill.max_timeout:
                        results = skill.activate(enemy, pc)
                    mact_counter = 0

                # Handling results
                for result in results:
                    dead_entity = result.get('dead')

                    if dead_entity:
                        G.combat_locked = False
                        if dead_entity != pc:
                            mact_counter = 0
                            pc.level_up_by(1)
                            G.endtext = Message("Victory!", colors.get('green'))

                        elif dead_entity == pc:
                            mact_counter = 0
                            G.endtext = Message("DEAD!", colors.get('red'))
                            G.over = True

            if not G.combat_locked:
                if user_input and user_input.key == 'ENTER':
                    if not G.over:
                        for skill in pc.skills:
                            skill.timeout = skill.max_timeout
                        if G.current_level == G.dungeon[-1]:
                            G.state = State.ENDING
                        else:
                            G.state = State.UPGD_PHASE
                        print("go")
                    else:
                        G.over = False
                        G.reset()
                        pc = G.return_player()
                        G.state = State.MENU

        elif G.state == State.ROOM_PHASE:
            if user_input and user_input.key == 'ENTER':
                if G.current_level.entity:
                    G.state = State.BATTLE_PHASE
                    G.combat_locked = True

        elif G.state == State.UPGD_PHASE:
            if user_input and user_input.key == 'ENTER':
                if G.upgd_selec:
                    pc.upgd_skillset(G.upgd_selec)
                    G.upgd_selec = ''
                    G.next_level()
                    G.state = State.ROOM_PHASE

        elif G.state == State.MENU:
            if user_input and user_input.key == 'ENTER':
                G.state = State.ROOM_PHASE

        elif G.state == State.ENDING:
            if user_input and user_input.key == 'ENTER':
                G.over = False
                G.reset()
                pc = G.return_player()
                G.state = State.MENU

        # Controls
        if user_input and user_input.key == 'ESCAPE':
            return True

        if user_input and user_input.key == 'ENTER' and user_input.alt:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()
