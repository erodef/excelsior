# coding=utf-8
"""
    TODO: More monsters, skills
    TODO: 1 more design pattern(decorators?)

    TODO: -EXTRA- Battle visuals (hit numbers, hit marks, warnings, different monster sprites etc)
    TODO: -EXTRA- Proper monster attacks and AI
    TODO: -EXTRA- Choices during dungeon movement
    TODO: -EXTRA- Combos
    TODO: -EXTRA- Music and sfx
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
    colors = Game.colors
    mact_counter = 0
    menu_cursor = 0

    # TDL init
    tdl.set_font(Game.font, greyscale=Game.greyscale, altLayout=Game.altLayout)
    root_console = tdl.init(Game.screen_width, Game.screen_height, title=Game.title)
    tdl.set_fps(30)

    # Console
    con = tdl.Console(Game.screen_width, Game.screen_height)

    # UI Panel
    hud = tdl.Console(Game.screen_width, Game.screen_height)

    # Message Log
    message_log = MessageLog(Game.message_x, Game.message_width, Game.message_height)


    # Player init
    pc = Game.return_player()

    if Game.starting:
        gamestate = State.MENU
        Game.gen_dungeon(Game.dungeon_levels)
        Game.starting = False

    # Draw
    while not tdl.event.is_window_closed():
        con.clear()

        # Drawing on screen in menu
        if gamestate == State.MENU:
            draw_menu(con, Game)

        # Drawing on screen in room
        if gamestate == State.ROOM_PHASE:
            draw_room(con, Game)

        # Drawing on screen during battle
        if gamestate == State.BATTLE_PHASE:
            draw_battle(con, Game, pc)

            root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)

        # Drawing on screen after battle
        if gamestate == State.UPGD_PHASE:
            draw_upgd(con, Game, pc)

        root_console.blit(con, 0, 0, Game.screen_width, Game.screen_height, 0, 0)
        tdl.flush()

        Game.mousedown = False
        # Handle events
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                Game.mouse = event.cell
                Game.mouse_x, Game.mouse_y = Game.mouse
            if event.type == 'MOUSEDOWN':
                Game.mousedown = True

        # If no input matches KEYDOWN, set user_input to None
        else:
            user_input = None

        # Handling events in diferent gamestates
        if gamestate == State.BATTLE_PHASE:
            enemy = Game.current_level.entity
            results = []
            if Game.combat_locked:
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

                    if dead_entity:
                        Game.combat_locked = False
                        if dead_entity != pc:
                            pc.absorb(1)
                            Game.endtext = Message("Victory!", colors.get('green'))

                        elif dead_entity == pc:
                            Game.endtext = Message("DEAD!", colors.get('red'))
                            Game.gameover = True

            if not Game.combat_locked:
                if user_input and user_input.key == 'ENTER':
                    if Game.gameover == False:
                        for skill in pc.skills:
                            skill.timeout = skill.max_timeout
                        message_log.messages = []
                        gamestate = State.UPGD_PHASE
                    else:
                        Game.gameover = False
                        Game.reset()
                        pc = Game.return_player()
                        gamestate = State.MENU

        elif gamestate == State.ROOM_PHASE:
            if user_input and user_input.key == 'ENTER':
                if Game.current_level.entity:
                    gamestate = State.BATTLE_PHASE
                    Game.combat_locked = True
                else:
                    Game.next_level()

        elif gamestate == State.UPGD_PHASE:
            if user_input and user_input.key == 'ENTER':
                if Game.upgd_selec:
                    pc.upgd_skillset(Game.upgd_selec)
                    Game.upgd_selec = ''
                    end = Game.next_level()
                    if not end == 1:
                        gamestate = State.ROOM_PHASE
                    else:
                        gamestate = State.ENDING

        elif gamestate == State.MENU:
            if user_input and user_input.key == 'ENTER':
                gamestate = State.ROOM_PHASE

        elif gamestate == State.ENDING:
            tmd = "You WIN!"
            con.draw_str(int(Game.screen_width/2)-int(len(tmd)/2),int(Game.screen_height/2)-5, tmd)
            kms = "Press Enter to continue..."
            con.draw_str(int(Game.screen_width/2)-int(len(kms)/2),int(Game.screen_height/2)-4, kms)
            if user_input and user_input.key == 'ENTER':
                Game.gameover = False
                Game.reset()
                pc = Game.return_player()
                gamestate = State.MENU

        # Controls
        if user_input and user_input.key == 'ESCAPE' :
            return True

        if user_input and user_input.key == 'ENTER' and user_input.alt :
            tdl.set_fullscreen(not tdl.get_fullscreen())

if __name__ == '__main__':
    main()
