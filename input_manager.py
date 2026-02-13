import pygame

# Centralized configuration - easy to change later!
KEYBOARD_CONTROLS = {
    "UP": [pygame.K_UP, pygame.K_w],
    "DOWN": [pygame.K_DOWN, pygame.K_s],
    "LEFT": [pygame.K_LEFT, pygame.K_a],
    "RIGHT": [pygame.K_RIGHT, pygame.K_d],
    "CONFIRM": [pygame.K_RETURN, pygame.K_SPACE],
    "PAUSE": [pygame.K_p],
    "BACK": [pygame.K_ESCAPE],
    "TOGGLE_MUSIC": [pygame.K_m],
    "TOGGLE_SFX": [pygame.K_f]
}
XBOX_CONTROLS_MOTION = {
    (0, 1) : "UP",
    (0, -1) : "DOWN",
    (-1, 0) : "LEFT",
    (1, 0) : "RIGHT"
}
XBOX_CONTROLS_BUTTONS = {
    0 : "CONFIRM",
    1 : "TOGGLE_MUSIC",
    2 : "TOGGLE_SFX",
    7 : "PAUSE",
    6: "BACK"
}

def get_input_action(event):
    """Translates any hardware event into a game action string."""
    
    # 1. Keyboard Mappings (Data-Driven)
    if event.type == pygame.KEYDOWN:
        for action, keys in KEYBOARD_CONTROLS.items():
            if event.key in keys:
                return action

    # 2. Xbox Controller Mappings (Hats/D-Pad)
    elif event.type == pygame.JOYHATMOTION:
        return XBOX_CONTROLS_MOTION.get(event.value)

    # 3. Xbox Controller Mappings (Buttons)
    elif event.type == pygame.JOYBUTTONDOWN:
        return XBOX_CONTROLS_BUTTONS.get(event.button)

    return None
