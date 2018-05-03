import tdl


def draw_menu(con, g):
    colors = g.colors
    title = "Excelsior"
    con.draw_str(int(g.screen_width / 2) - int(len(title) / 2), int(g.screen_height / 2) - 10, title)

    con.draw_str(int(g.screen_width / 2) - 6, int(g.screen_height / 2), '[ENTER] Start')
    con.draw_str(int(g.screen_width / 2) - 5, int(g.screen_height / 2), 'ENTER', fg=colors.get('green'))

    con.draw_str(int(g.screen_width / 2) - 5, int(g.screen_height / 2) + 1, '[ESC] Quit')
    con.draw_str(int(g.screen_width / 2) - 4, int(g.screen_height / 2) + 1, 'ESC', fg=colors.get('green'))


def draw_room(con, g):
    colors = g.colors
    con.draw_str(2, 2, g.current_level.name)
    con.draw_str(3, 4, g.current_level.desc)

    if g.current_level.entity:
        con.draw_str(3, 8, "In this room, there is a")
        con.draw_str(28, 8, g.current_level.entity.name, colors.get('red'))

    # Bottom Panel
    con.draw_str(g.screen_width - 20, g.screen_height - 1, '[ENTER] Fight')
    con.draw_str(g.screen_width - 19, g.screen_height - 1, 'ENTER', fg=colors.get('green'))


def draw_upgd(con, g, pc):
    colors = g.colors
    con.clear()

    con.draw_str(int(g.screen_width / 2), 1, 'Enhancement')
    con.draw_str(3, 3, 'Upgrade your skills or acquire new ones.')

    mouse_x, mouse_y = g.mouse
    alist = []
    plist = []
    x = 2
    y = 15
    con.draw_str(x, y, 'Available skills:')
    y += 1
    for skill in pc.skills:
        plist.append((x, y))
        alist.append(skill)
        con.draw_str(x, y, ' -' + skill.name)
        y += 1
    for skill in g.skill_database:
        for pskill in pc.skills:
            if pskill.t_name == skill.req:
                con.draw_str(x, y, ' -' + skill.name)
                plist.append((x, y))
                alist.append(skill)
                y += 1

    x = 2
    y = 30
    for pos in plist:
        ui_skill = alist[plist.index(pos)]
        pos_x, pos_y = pos
        if mouse_y == pos_y and pos_x <= mouse_x <= pos_x + len(ui_skill.name) + 2:
            g.upgd_selec = ui_skill

    if g.upgd_selec:
        con.draw_str(x, y, g.upgd_selec.name + " LVL." + str(g.upgd_selec.level))
        con.draw_str(x, y + 2, g.upgd_selec.desc)
        y += 4
        for effect in g.upgd_selec.effects():
            con.draw_str(x, y, effect)
            y += 1

    con.draw_str(g.screen_width - 20, g.screen_height - 1, '[ENTER] Next')
    con.draw_str(g.screen_width - 19, g.screen_height - 1, 'ENTER', colors.get('green'))


def draw_battle(con, g, pc):
    colors = g.colors
    con.clear()
    con.draw_str(2, 2, g.current_level.name)

    enemy = g.current_level.entity

    # HUDs
    draw_bg_hud(con, g.pc_hud_x, g.pc_hud_y, colors)

    # Player
    con.draw_str(g.pc_hud_x + 14, g.pc_hud_y, pc.name)
    render_bar(con, g.pc_hud_x + 3, g.pc_hud_y + 4, 28, 3, pc.hp, pc.max_hp, colors.get('red'),
               colors.get('darker_red'), colors.get('white'))

    # Enemy
    en_hp_bar = 40
    con.draw_str(g.en_hud_x + int(en_hp_bar / 2) - int(len(enemy.name) / 2), g.en_hud_y, enemy.name)
    render_bar(con, g.en_hud_x, g.en_hud_y + 2, en_hp_bar, 3, enemy.hp, enemy.max_hp, colors.get('red'),
               colors.get('darker_red'), colors.get('white'))

    # Skills
    # Player
    skill_bar_width = 10
    x = g.pc_hud_x + 3
    y = g.pc_hud_y + 8
    n = 1
    for skill in pc.skills:
        if pc.skills.index(skill) == 2:
            y -= 6
            x += 15
        con.draw_str(x, y, skill.name)
        con.draw_str(x, y + 1, "[?]")
        con.draw_str(x + 1, y + 1, str(n), fg=colors.get('green'))
        render_bar(con, x + 4, y + 1, skill_bar_width, 1, skill.timeout, skill.max_timeout, colors.get('green'),
                   colors.get('darker_green'), colors.get('black'))
        y += 3
        n += 1

    x = g.pc_hud_x + 9
    y = g.pc_hud_y + 2
    for buff in pc.buffs:
        con.draw_str(x, y, buff.icon, fg=colors.get('green'))
        x += 1

    skill_bar_width = 30
    x = int(g.screen_width / 2) - int(skill_bar_width / 2)
    y = g.en_hud_y + 5
    for skill in enemy.skills:
        render_bar(con, x, y + 1, skill_bar_width, 1, skill.timeout, skill.max_timeout, colors.get('green'),
                   colors.get('darker_green'), colors.get('black'))

    x = g.en_hud_x - 1
    y = g.en_hud_y
    for buff in enemy.buffs:
        con.draw_str(x, y, buff.icon, fg=colors.get('green'))
        y += 1

    # Enemy Sprite
    draw_enemy_battler(con, "data/sprites/" + enemy.battler + ".txt", int(g.screen_width / 2) - 15, 12)

    # End result
    if not g.combat_locked:
        kms = "Press Enter to continue..."
        con.draw_str(int(g.screen_width / 2) - int(len(kms) / 2), int(g.screen_height / 2) + 1, kms)
        con.draw_str(int(g.screen_width / 2) - int(len(g.endtext.text) / 2), int(g.screen_height / 2),
                     g.endtext.text, g.endtext.color)


def draw_bg_hud(con, ix, iy, colors):
    """Draws background elements on HUD."""
    con.draw_frame(0, 30, None, None, string="/", bg=colors.get('black'))


def draw_enemy_battler(con, path, ix, iy):
    """Draws enemy sprite."""
    with open(path, 'r') as data:
        chara = ' '
        x = ix
        y = iy
        for line in data:
            for character in line:
                if character == '.':
                    chara = ' '
                elif character == 'F':
                    chara = 'F'
                con.draw_char(x, y, chara)
                x += 1
            x = ix
            y += 1


def draw_ending(con, g):
    tmd = "You WIN!"
    con.draw_str(int(g.screen_width / 2) - int(len(tmd) / 2), int(g.screen_height / 2) - 5, tmd)
    kms = "Press Enter to continue..."
    con.draw_str(int(g.screen_width / 2) - int(len(kms) / 2), int(g.screen_height / 2) - 4, kms)


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
        draw_y += 1

    # Text and values
    text = str(value) + '/' + str(maximum)
    x_centered = x + int((total_width - len(text)) / 2)
    y_centered = y + int(total_height / 2)

    panel.draw_str(x_centered, y_centered, text, fg=string_color, bg=None)


def clear_screen(con, screen_width, screen_height):
    # Clean all console positions
    for y in range(screen_height):
        for x in range(screen_width):
            con.draw_char(x, y, ' ', bg=None)


def draw_colored_line(con, x, y, text, fg=None, bg=None):
    con = tdl.Console(2, 2)
    colored_words = []
    colors = []
    
    n = 0
    for chara in text:
        if chara is "[":
            word = ""
            for charac in text[n+1:]:
                if charac is not "]":
                    word += charac
                else:
                    colored_words.append(word)
                    break
        n += 1
    # con.draw_str(x, y, text, fg, bg)
    return colored_words, colors