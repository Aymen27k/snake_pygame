import pygame

# Centralized configuration - easy to change later!
KEYBOARD_CONTROLS = {
    "UP": [pygame.K_UP, pygame.K_w],
    "DOWN": [pygame.K_DOWN, pygame.K_s],
    "LEFT": [pygame.K_LEFT, pygame.K_a],
    "RIGHT": [pygame.K_RIGHT, pygame.K_d],
    "CONFIRM": [pygame.K_RETURN],
    "SHOOT" : [pygame.K_SPACE],
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
XBOX_CONTROLS_ANALOG = {
    "LEFT":  lambda x, y: x < -0.5,
    "RIGHT": lambda x, y: x > 0.5,
    "UP":    lambda x, y: y < -0.5,
    "DOWN":  lambda x, y: y > 0.5
}

XBOX_CONTROLS_BUTTONS = {
    0 : "CONFIRM",
    1 : "TOGGLE_MUSIC",
    2 : "TOGGLE_SFX",
    7 : "PAUSE",
    6: "BACK"
}
FRIENDLY_NAMES = {
    "RETURN": "ENTER",
    "ESCAPE": "ESC",
    "UP": "ARROW UP",
    "DOWN": "ARROW DOWN",
    "LEFT": "ARROW LEFT",
    "RIGHT": "ARROW RIGHT",
    "SPACE" : "SPACE BAR",
    "M": "M (Music)",
    "F": "F (SFX)",
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

    # 4. Xbox Controller Mappings (Analog Stick)
    elif event.type == pygame.JOYAXISMOTION:
        joystick = pygame.joystick.Joystick(event.joy)
        x = joystick.get_axis(0)  # left stick horizontal
        y = joystick.get_axis(1)  # left stick vertical

        for action, condition in XBOX_CONTROLS_ANALOG.items():
            if condition(x, y):
                return action


        return None

def get_control_schemes():
    """Returns a list of strings representing the current bindings."""
    schemes = []
    for action, keys in KEYBOARD_CONTROLS.items():
        key_name = pygame.key.name(keys[0]).upper()
        schemes.append(f"{action}: {key_name}")
    return schemes

def get_human_key_name(pygame_name):
    # If it's in our dictionary, use the friendly name.
    return FRIENDLY_NAMES.get(pygame_name.upper(), pygame_name.upper())