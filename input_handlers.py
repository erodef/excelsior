def handle_keys(user_input):
    # Movement
    if user_input.keychar == 'z':
        return {'z_press': True}

    # Fullscreen (Alt+Enter)
    if user_input.key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}

    # Exit
    elif user_input.key == 'ESCAPE':
        return {'quit': True}

    # If nothing pressed, return nothing
    return {}
