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

    combat_locked = False
    turn = 0

    # TDL init
    tdl.set_font(Game.font, greyscale=Game.greyscale, altLayout=Game.altLayout)
    root_console = tdl.init(Game.screen_width, Game.screen_height, title=Game.title)

    # Gameplay screen
    con = tdl.Console(Game.screen_width, Game.screen_height)

    # UI Panel
    hud = tdl.Console(Game.screen_width, Game.screen_height)

    Game.gen_dungeon(5)

    # Player init
    pskills = [getSkill('punch'), getSkill('kick'), getSkill('scratch')]
    pc_fighter = Fighter(hp=50, sp=10, atk=15, df=10, spd=15, skills=pskills)
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

            # Player
            con.draw_str(Game.pc_hud_x, Game.pc_hud_y, pc.name)
            render_bar(con, Game.pc_hud_x, Game.pc_hud_y+2, Game.bar_width, 'HP', pc.fighter.hp, pc.fighter.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))
            render_bar(con, Game.pc_hud_x, Game.pc_hud_y+3, Game.bar_width, 'SP', pc.fighter.sp, pc.fighter.max_sp, colors.get('blue'), colors.get('dark_blue'), colors.get('white'))

            # Enemy
            con.draw_str(Game.en_hud_x, Game.en_hud_y, Game.current_level.entity.name)
            render_bar(con, Game.en_hud_x, Game.en_hud_y+2, Game.bar_width, 'HP', Game.current_level.entity.fighter.hp, Game.current_level.entity.fighter.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))
            render_bar(con, Game.en_hud_x, Game.en_hud_y+3, Game.bar_width, 'SP', Game.current_level.entity.fighter.sp, Game.current_level.entity.fighter.max_sp, colors.get('blue'), colors.get('dark_blue'), colors.get('white'))

            y = message_log.height
            for message in message_log.messages:
                con.draw_str(message_log.x, y, message.text, fg=message.color)
                y += 1

            con.draw_str(40, Game.screen_height-3, '[1]')
            con.draw_str(44, Game.screen_height-3, pc.fighter.skills[0].name)
            con.draw_str(50, Game.screen_height-3, str(pc.fighter.skills[0].timeout)+'/'+str(pc.fighter.skills[0].max_timeout))

            con.draw_str(40, Game.screen_height-2, '[2]')
            con.draw_str(44, Game.screen_height-2, pc.fighter.skills[1].name)


            con.draw_str(40, Game.screen_height-1, '[3]')
            con.draw_str(44, Game.screen_height-1, pc.fighter.skills[2].name)


            root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

        # -------------------------------

        if gamestate == State.UPGD_PHASE:
            con.clear()

            con.draw_str(1, 1, 'Status:')
            con.draw_str(10, 1, pc.name)

            con.draw_str(1, 6, 'Skills')
            y = 8
            for skill in pc.fighter.skills:
                con.draw_str(1, y, ' -'+ skill.name)
                y += 1

            con.draw_str(20, 6, 'Souls:')
            con.draw_str(28, 6, str(pc.soulstack))

            con.draw_str(2, Game.screen_height-1, '[Z] Next')

        # -------------------------------

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

        # If there is no input, continue checking. This means
        # the game only continues if there's user input (Keypress).
        if not user_input:
            continue

        # Input actions

        action = handle_keys(user_input)
        quit = action.get('quit')
        fullscreen = action.get('fullscreen')
        z_press = action.get('z_press')

        # Combat
        if gamestate == State.BATTLE_PHASE:
            enemy = Game.current_level.entity
            results = []
            if combat_locked:
                for skill in pc.fighter.skills:
                    if skill.timeout < skill.max_timeout:
                        skill.timeout += 1

                if user_input.keychar == '1':
                    if pc.fighter.skills[0].timeout == pc.fighter.skills[0].max_timeout:
                        results = pc.fighter.attack(enemy, pc.fighter.skills[0])

                """
                results = enemy.fighter.attack(pc, random.choice(enemy.fighter.skills))
                """

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
                if user_input.keychar == 'z':
                    message_log.messages = []
                    gamestate = State.UPGD_PHASE

        # Controls
        if z_press and gamestate == State.ROOM_PHASE:
            if Game.current_level.entity:
                gamestate = State.BATTLE_PHASE
                combat_locked = True
            else:
                Game.next_level()

        elif z_press and gamestate == State.UPGD_PHASE:
            Game.next_level()
            gamestate = State.ROOM_PHASE

        if quit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

if __name__ == '__main__':
    main()
