import enum


FONT = "roboto"
FONT_SIZE = 15


class orient(enum.Enum):

    horizontal = 0
    vertical = 1


class state(enum.Enum):

    default = 0
    hover = 1
    pressed = 2


class colors:

    default = (255, 255, 255)
    hover = (200, 200, 200)
    pressed = (150, 150, 150)
    border = (200, 200, 200)

    tick_border = (0, 0, 0)
    tick_default = (230, 230, 230)
    tick_hover = (180, 180, 180)
    tick_pressed = (130, 130, 130)
    tick_default_choosed = (255, 0 , 0)
    tick_hover_choosed = (180, 0, 0)
    tick_pressed_choosed = (130, 0, 0)

    splitter = (100, 100, 100)

    menu_background = (255, 255, 255)

    text = (0, 0, 0)