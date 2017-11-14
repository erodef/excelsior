def draw_entity(con, entity, fov):
    # Draw entity onto console
    if fov[entity.px, entity.py]:
        con.draw_char(entity.px, entity.py, entity.tile, entity.color, bg=entity.bg)

def clear_entity(con, entity):
    # Erase the character that represents this object
    con.draw_char(entity.px, entity.py, ' ', entity.color, bg=None)

# Get names of entities at mouse location if they're visible
def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.px == x and entity.py == y and game_map.fov[entity.px, entity.py]]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Text and values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def clear_all(con, entities, player):
    # Clear all entities in the list from console
    for entity in entities:
        clear_entity(con, entity)
    # clear_entity(con, player)

def clear_screen(con, screen_width, screen_height):
    # Clean all console positions
    for y in range(screen_height):
        for x in range(screen_width):
            con.draw_char(x, y, ' ', bg=None)

def draw_skillbtn(con):
    pass
