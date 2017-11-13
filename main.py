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
    panel = tdl.Console(Game.screen_width, Game.panel_height)

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

        # Bottom Panel
        panel_bg = colors.get('lighter_black')
        panel.clear(bg=panel_bg)

        if gamestate == State.ROOM_PHASE:
            if Game.current_level.entity:
                con.draw_str(3, 8, "In this room, there is a")
                con.draw_str(28, 8, Game.current_level.entity.name, colors.get('red'))

            # Bottom Panel
            panel.draw_str(2, 2, '[Z] Fight', bg=panel_bg, fg=colors.get('green'))

        if gamestate == State.BATTLE_PHASE:
            con.clear()
            combat_locked = True

            con.draw_str(4, 5,pc.name.capitalize())
            render_bar(con, 4, 7, 20, 'HP', pc.fighter.hp, pc.fighter.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))
            render_bar(con, 4, 8, 20, 'SP', pc.fighter.sp, pc.fighter.max_sp, colors.get('blue'), colors.get('dark_blue'), colors.get('white'))

            con.draw_str(56, 5,Game.current_level.entity.name.capitalize())
            render_bar(con, 56, 7, 20, 'HP', Game.current_level.entity.fighter.hp, Game.current_level.entity.fighter.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))
            render_bar(con, 56, 8, 20, 'SP', Game.current_level.entity.fighter.sp, Game.current_level.entity.fighter.max_sp, colors.get('blue'), colors.get('dark_blue'), colors.get('white'))

            y = message_log.height
            for message in message_log.messages:
                con.draw_str(message_log.x, y, message.text, fg=message.color)
                y += 1

            root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

            panel.draw_str(2, 2, '[1] Attack', bg=panel_bg)
            panel.draw_str(2, 3, '[2] Guard', bg=panel_bg)
            panel.draw_str(2, 4, '[3] Evade', bg=panel_bg)

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

            panel.draw_str(2, 2, '[Z] Next', bg=panel_bg)

        # -------------------------------

        root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)
        root_console.blit(panel, 0, Game.panel_y, Game.screen_width,
                          Game.panel_height, 0, 0)
        
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
            if turn == 0 and user_input.keychar == '1':
                results = pc.fighter.attack(enemy, pc.fighter.skills[0])
                turn = 1
            elif turn == 1:
                results = enemy.fighter.attack(pc, pc.fighter.skills[0])
                turn = 0
            
            for result in results:
                message = result.get('message')
                if message:
                    message_log.add_message(message)
            
            if enemy.fighter.hp <= 0:
                turn = 0
                combat_locked = False
                message_log.messages = []
                gamestate = State.UPGD_PHASE

        # Controls
        if z_press and gamestate == State.ROOM_PHASE:
            if Game.current_level.entity:
                gamestate = State.BATTLE_PHASE
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
