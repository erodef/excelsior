
def draw_menu(con, Game):
    colors = Game.colors
    title = "Excelsior"
    con.draw_str(int(Game.screen_width/2)-int(len(title)/2), int(Game.screen_height/2)-10, title)

    con.draw_str(int(Game.screen_width/2)-6, int(Game.screen_height/2), '[ENTER] Start')
    con.draw_str(int(Game.screen_width/2)-5, int(Game.screen_height/2), 'ENTER', fg=colors.get('green'))

    con.draw_str(int(Game.screen_width/2)-5, int(Game.screen_height/2)+1, '[ESC] Quit')
    con.draw_str(int(Game.screen_width/2)-4, int(Game.screen_height/2)+1, 'ESC', fg=colors.get('green'))

def draw_room(con, Game):
    colors = Game.colors
    con.draw_str(2, 2, Game.current_level.name)
    con.draw_str(3, 4, Game.current_level.desc)

    if Game.current_level.entity:
        con.draw_str(3, 8, "In this room, there is a")
        con.draw_str(28, 8, Game.current_level.entity.name, colors.get('red'))

    # Bottom Panel
    con.draw_str(Game.screen_width-20, Game.screen_height-1, '[ENTER] Fight')
    con.draw_str(Game.screen_width-19, Game.screen_height-1, 'ENTER', fg=colors.get('green'))

def draw_upgd(con, Game, pc):
    colors = Game.colors
    con.clear()

    con.draw_str(int(Game.screen_width/2), 1, 'Enhancement')
    con.draw_str(3, 3, 'Upgrade your skills or acquire new ones.')
    con.draw_str(3, 4, 'Most skills will stay hidden until you unlock them through other ones.')

    con.draw_str(3, 5, 'Mouse over the skill name for details.')

    mouse_x, mouse_y = Game.mouse
    alist = []
    plist = []
    x = 2
    y = 15
    con.draw_str(x, y, 'Known skills:')
    y += 1
    for skill in pc.skills:
        con.draw_str(x, y, ' -'+ skill.name)
        y += 1

    x = int(Game.screen_width/2)
    y = 15
    con.draw_str(x, y, 'Available skills:')
    y += 1
    for skill in Game.skill_database:
        for pskill in pc.skills:
            if pskill.t_name == skill.req:
                con.draw_str(x, y, ' -'+ skill.name)
                plist.append((x,y))
                alist.append(skill)
                y += 1

    x = 2
    y = 30
    for pos in plist:
        ui_skill = alist[plist.index(pos)]
        pos_x, pos_y = pos
        if mouse_y == pos_y and mouse_x >= pos_x and mouse_x <= pos_x + len(ui_skill.name)+2:
            con.draw_str(x, y, ui_skill.name)
            con.draw_str(x, y+2, ui_skill.desc)
            if Game.mousedown:
                Game.upgd_selec = ui_skill

    if Game.upgd_selec:
        con.draw_str(15, 29, "You selected "+Game.upgd_selec.name)

    con.draw_str(Game.screen_width-20, Game.screen_height-1, '[ENTER] Next')
    con.draw_str(Game.screen_width-19, Game.screen_height-1, 'ENTER', colors.get('green'))

def draw_battle(con, Game, pc):
    colors = Game.colors
    con.clear()
    con.draw_str(2, 2, Game.current_level.name)

    enemy = Game.current_level.entity

    # HUDs
    draw_bg_hud(con, Game.pc_hud_x, Game.pc_hud_y, colors)

    # Player
    con.draw_str(Game.pc_hud_x+14, Game.pc_hud_y, pc.name)
    render_bar(con, Game.pc_hud_x+3, Game.pc_hud_y+4, 28, 3, pc.hp, pc.max_hp, colors.get('red'), colors.get('darker_red'), colors.get('white'))

    # Enemy
    en_hp_bar = 40
    con.draw_str(Game.en_hud_x+int(en_hp_bar/2)-int(len(enemy.name)/2), Game.en_hud_y, enemy.name)
    render_bar(con, Game.en_hud_x, Game.en_hud_y+2, en_hp_bar, 3, enemy.hp, enemy.max_hp, colors.get('red'), colors.get('darker_red'), colors.get('white'))

    # Skills
    # Player
    skill_bar_width = 10
    x = Game.pc_hud_x+3
    y = Game.pc_hud_y+8
    n = 1
    for skill in pc.skills:
        con.draw_str(x, y, skill.name)
        con.draw_str(x, y+1, "[?]")
        con.draw_str(x+1, y+1, str(n), fg= colors.get('green'))
        render_bar(con, x+4, y+1, skill_bar_width, 1, skill.timeout, skill.max_timeout, colors.get('green'), colors.get('darker_green'), colors.get('black'))
        y += 3
        n += 1

    x = Game.pc_hud_x+9
    y = Game.pc_hud_y+2
    for buff in pc.buffs:
        con.draw_str(x, y, buff.icon, fg=colors.get('green'))
        x+=1

    # Enemy
    x = Game.en_hud_x
    y = Game.en_hud_y+5
    n = 1
    for skill in enemy.skills:
        con.draw_str(x, y, skill.name)
        render_bar(con, x, y+1, skill_bar_width, 1, skill.timeout, skill.max_timeout, colors.get('green'), colors.get('darker_green'), colors.get('black'))
        y += 2
        n += 1

    x = Game.en_hud_x-1
    y = Game.en_hud_y
    for buff in enemy.buffs:
        con.draw_str(x, y, buff.icon, fg=colors.get('green'))
        y+=1

    # Enemy Sprite
    draw_enemy_battler(con, "skel.txt", int(Game.screen_width/2)-15, 12)

    # End result
    if not Game.combat_locked:
        kms = "Press Enter to continue..."
        con.draw_str(int(Game.screen_width/2)-int(len(kms)/2), int(Game.screen_height/2)+1, kms)
        con.draw_str(int(Game.screen_width/2)-int(len(Game.endtext.text)/2), int(Game.screen_height/2), Game.endtext.text, Game.endtext.color)

def draw_bg_hud(con, ix, iy, colors):
    # Player element
    with open('ui_bg_player.txt', 'r') as data:
        color = ''
        x = ix
        y = iy
        for line in data:
            for character in line:
                if character == '1':
                    color = colors.get('orange')
                else:
                    color = colors.get('black')
                con.draw_char(x, y, ' ', bg=color)
                x += 1
            x = ix
            y += 1

def draw_enemy_battler(con, path, ix, iy):
    # Enemy sprite
    with open(path, 'r') as data:
        chara = ' '
        x = ix
        y = iy
        for line in data:
            for character in line:
                if character == 'F':
                    chara = 'F'
                elif character == '.':
                    chara = ' '
                con.draw_char(x, y, chara)
                x += 1
            x = ix
            y += 1

def render_bar(panel, x, y, total_width, total_height, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)
    draw_y = y
    # Render the background first
    for number in range(total_height):
        panel.draw_rect(x, draw_y, total_width, 1, None, bg=back_color)

        # Now render the bar on top
        if bar_width > 0:
            panel.draw_rect(x, draw_y, bar_width, 1, None, bg=bar_color)
        draw_y +=1

    # Text and values
    text = str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)
    y_centered = y + int(total_height / 2)

    panel.draw_str(x_centered, y_centered, text, fg=string_color, bg=None)

def clear_screen(con, screen_width, screen_height):
    # Clean all console positions
    for y in range(screen_height):
        for x in range(screen_width):
            con.draw_char(x, y, ' ', bg=None)
