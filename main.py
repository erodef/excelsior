# coding=utf-8
"""
    TODO: Skill upgrade progression system
    TODO: Introduction
    TODO: Ending

    TODO: -EXTRA- Choices during dungeon movement
    TODO: -EXTRA- More monsters, skills
    TODO: -EXTRA- Music and sfx
    TODO: -EXTRA- Animations
"""
import json
import random
import tdl
import sys
import copy
from components.enemy_ai import *
from game_states import *
from engine import *
from rendering import *
from logbox import *
from pc import *
from skill import *
from data_parser import *
from colors import getColors


def main():

    Game = Engine()
    colors = getColors()

    combat_locked = False
    mact_counter = 0

    # TDL init
    tdl.set_font(Game.font, greyscale=Game.greyscale, altLayout=Game.altLayout)
    root_console = tdl.init(Game.screen_width, Game.screen_height, title=Game.title)
    tdl.set_fps(30)

    # Gameplay screen
    con = tdl.Console(Game.screen_width, Game.screen_height)

    # UI Panel
    hud = tdl.Console(Game.screen_width, Game.screen_height)

    Game.gen_dungeon(5)

    # Player init
    pskills = [copy.deepcopy(Game.skill_database[0]), copy.deepcopy(Game.skill_database[1]), copy.deepcopy(Game.skill_database[2])]
    pc_fighter = {'hp':50, 'atk':15, 'df':10, 'spd':15, 'skills':pskills}
    pc = PC('Player', fighter=pc_fighter)

    gamestate = State.ROOM_PHASE

    message_log = MessageLog(Game.message_x, Game.message_width, Game.message_height)

    if Game.starting:
        Game.starting = False

    # Draw
    while not tdl.event.is_window_closed():
        con.clear()

        con.draw_str(2, 2, Game.current_level.name)
        con.draw_str(3, 4, Game.current_level.desc)

        if gamestate == State.ROOM_PHASE:
            if Game.current_level.entity:
                con.draw_str(3, 8, "In this room, there is a")
                con.draw_str(28, 8, Game.current_level.entity.name, colors.get('red'))

            # Bottom Panel
            con.draw_str(2, Game.screen_height-1, '[ ] Fight')
            con.draw_str(3, Game.screen_height-1, 'Z', fg=colors.get('green'))

        if gamestate == State.BATTLE_PHASE:
            con.clear()
            con.draw_str(2, 2, Game.current_level.name)

            enemy = Game.current_level.entity

            # HUDs
            # Player
            con.draw_str(Game.pc_hud_x, Game.pc_hud_y, pc.name)
            render_bar(con, Game.pc_hud_x, Game.pc_hud_y+2, Game.bar_width, 'HP', pc.hp, pc.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))

            # Enemy
            con.draw_str(Game.en_hud_x, Game.en_hud_y, enemy.name)
            render_bar(con, Game.en_hud_x, Game.en_hud_y+2, Game.bar_width, 'HP', enemy.hp, enemy.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))

            # Log
            y = 15
            for message in message_log.messages:
                con.draw_str(message_log.x, y, message.text, fg=message.color)
                y += 1

            # Skills
            # Player
            x = Game.pc_hud_x
            y = Game.pc_hud_y+5
            n = 1
            for skill in pc.skills:
                con.draw_str(x, y, "["+str(n)+"]")
                render_bar(con, x+4, y, 20, skill.name, skill.timeout, skill.max_timeout, colors.get('green'), colors.get('darker_green'), colors.get('black'))
                y += 1
                n += 1

            # Enemy
            x = Game.en_hud_x
            y = Game.en_hud_y+5
            n = 1
            for skill in enemy.skills:
                con.draw_str(x, y, "["+str(n)+"]")
                render_bar(con, x+4, y, 20, skill.name, skill.timeout, skill.max_timeout, colors.get('green'), colors.get('darker_green'), colors.get('black'))
                y += 1
                n += 1

            # Buffs
            # Player
            x = 35
            y = 5
            for buff in pc.buffs:
                con.draw_str(x, y, buff.icon, fg=colors.get('green'))
                y+=1

            # Enemy
            x = 65
            y = 5
            for buff in enemy.buffs:
                con.draw_str(x, y, buff.icon, fg=colors.get('green'))
                y+=1

            # Battlers
            # Player
            lx = 12
            ly = 25
            for bx in range(10):
                for by in range(10):
                    con.draw_char(bx+lx, by+ly, '@')

            # Enemy
            lx = 56
            ly = 25
            for bx in range(10):
                for by in range(10):
                    con.draw_char(bx+lx, by+ly, 'Y')

            root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

        if gamestate == State.UPGD_PHASE:
            con.clear()

            con.draw_str(1, 1, 'Status:')
            con.draw_str(10, 1, pc.name)

            con.draw_str(1, 6, 'Skills')
            y = 8
            for skill in pc.skills:
                con.draw_str(1, y, ' -'+ skill.name)
                y += 1

            con.draw_str(20, 6, 'Points:')
            con.draw_str(28, 6, str(pc.soulstack))

            con.draw_str(2, Game.screen_height-1, '[Z] Next')

        root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

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

        # Input actions

        # Combat
        if gamestate == State.BATTLE_PHASE:
            enemy = Game.current_level.entity
            results = []
            if combat_locked:
                # Player
                for skill in pc.skills:
                    if skill.timeout < skill.max_timeout:
                        skill.timeout += 1

                for buff in pc.buffs:
                    if buff.timeout > 0:
                        buff.timeout -= 1
                    else:
                        del pc.buffs[pc.buffs.index(buff)]

                if user_input:
                    if user_input.keychar == '1' or user_input.keychar == '2' or user_input.keychar == '3' or user_input.keychar == '4':
                        skill = pc.skills[int(user_input.keychar)-1]
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
                    message = result.get('message')
                    dead_entity = result.get('dead')
                    if message:
                        message_log.add_message(message)

                    if dead_entity and dead_entity != pc:
                        message_log.add_message(Message(dead_entity.name+ " has died!"))
                        message_log.add_message(Message("Press 'Z' to continue..."))
                        combat_locked = False

            if not combat_locked:
                if user_input and user_input.keychar == 'z':
                    for skill in pc.skills:
                        skill.timeout = skill.max_timeout
                    message_log.messages = []
                    gamestate = State.UPGD_PHASE

        # Controls
        elif user_input and user_input.keychar == 'z' and gamestate == State.ROOM_PHASE:
            if Game.current_level.entity:
                gamestate = State.BATTLE_PHASE
                combat_locked = True
            else:
                Game.next_level()

        elif user_input and user_input.keychar == 'z' and gamestate == State.UPGD_PHASE:
            Game.next_level()
            gamestate = State.ROOM_PHASE

        if user_input and user_input.key == 'ESCAPE' :
            return True

        if user_input and user_input.key == 'ENTER' and user_input.alt :
            tdl.set_fullscreen(not tdl.get_fullscreen())

if __name__ == '__main__':
    main()
