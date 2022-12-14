import pygame
from random import randint
from widgets import Widget, Button, CombinedButtonsH, BoxLayoutH, Menu
from widgets.field import Field, colors
from widgets.language_pack import Default, Ukrainian


class Game:

    def __init__(self, cols: int, rows: int, size: int):

        self.display = pygame.display.set_mode((cols*size, rows*size), pygame.RESIZABLE)
        pygame.display.set_caption("Game of Life")
        
        self.field = Field(cols*size, rows*size, size, self.display)
        self.alive_probability = 0.4
        self.buttons_size = 47
        self.processing = False
        self.interacted = False
        self.shift_pressed = False

        self.language = Default()
        self.init_widgets(*self.display.get_size())     


    def init_widgets(self, width: int, height: int):

        self.widgets: list[Widget] = []
        self.widgets.append(self.field)

        x = (width - 12 * self.buttons_size - 40) // 2
        y = height - self.buttons_size - 10
        panel = BoxLayoutH(x, y, self.buttons_size)
        empty = Widget(width=10)

        start_button_text = self.language.START_BUTTON if not self.processing else self.language.START_BUTTON_PAUSE
        self.start_button = Button(start_button_text, width=self.buttons_size*3//2)
        self.start_button.bind(self.change_processing)
        randomise_button = Button(self.language.RANDOMISE_BUTTON, width=self.buttons_size*5//2)
        randomise_button.bind(self.generate_field)
        clear_button = Button(self.language.CLEAR_BUTTON, width=self.buttons_size*2)
        clear_button.bind(self.clear_field)
        panel.add_widgets(randomise_button, empty, clear_button, empty, self.start_button)

        fps_buttons = CombinedButtonsH()
        sub_fps = Button(self.language.SUBTRACT_FPS_BUTTON)
        sub_fps.bind(self.subtract_fps)
        add_fps = Button(self.language.ADD_FPS_BUTTON)
        add_fps.bind(self.add_fps)
        max_fps = Button(self.language.MAX_FPS_BUTTON)
        max_fps.bind(self.set_maxfps)
        fps_buttons.add_buttons(sub_fps, add_fps, max_fps)
        panel.add_widgets(empty, fps_buttons)

        cell_buttons = CombinedButtonsH()
        inc = Button(self.language.INCREASE_SCALE_BUTTON, width=self.buttons_size*3//2)
        inc.bind(self.increase_scale)
        dec = Button(self.language.DECREASE_SCALE_BUTTON, width=self.buttons_size*3//2)
        dec.bind(self.decrease_scale)
        cell_buttons.add_buttons(inc, dec)
        panel.add_widgets(empty, cell_buttons)

        self.widgets.append(panel)

        self.menu = Menu(self.field, 0, 0, height, self.buttons_size, self.display, self.language)
        self.widgets.append(self.menu)

        lang_button = Button(
            self.language.CHANGE_LANGUAGE_BUTTON,
            self.display.get_width()-self.buttons_size-10,
            10,
            self.buttons_size, self.buttons_size
            )
        lang_button.bind(self.change_language)
        self.widgets.append(lang_button)


    def change_processing(self):

        self.processing = not self.processing
        if self.processing:
            self.start_button.text = self.language.START_BUTTON_PAUSE
        else:
            self.start_button.text = self.language.START_BUTTON


    def add_fps(self):

        self.field.fps += self.field.fps_step


    def subtract_fps(self):

        if self.field.fps <= self.field.fps_step: self.field.fps = self.field.fps_step
        else: self.field.fps -= self.field.fps_step


    def set_maxfps(self):

        if self.field.fps == 0: self.field.fps = self.field.fps_step
        else: self.field.fps = 0


    def clear_field(self):

        for x in range(self.field.cols):
            for y in range(self.field.rows):
                self.field.cells[x][y].state = False
                self.field.cells[x][y].state_next = False
                self.field.cells[x][y].neighbours = 0
                self.field.cells[x][y].neighbours_next = 0
                color = colors.dead
                self.field.draw_cell(x, y, color)


    def generate_field(self):

        for x in range(self.field.cols):
            for y in range(self.field.rows):
                probability = randint(1, 1000) / 1000
                res = probability <= self.alive_probability
                self.field.set_cell_state(x, y, res)
                color = colors.alive if self.field.cells[x][y].state else colors.dead
                self.field.draw_cell(x, y, color)


    def increase_scale(self):

        value = (self.field.cell_size + 5) // 6
        self.field.increase_cell_size(value, self.display)


    def decrease_scale(self):

        value = (self.field.cell_size + 5) // 6
        self.field.decrease_cell_size(value, self.display)


    def draw_widgets(self):

        for widget in self.widgets:
            widget.draw(self.display)


    def process_intereaction(self):

        self.interacted = False
        for widget in reversed(self.widgets):
            self.interacted = widget.check_interaction(self.interacted)


    def resize(self):
        
        self.field.resize(self.display)
        self.field.shift(0, 0)
        self.init_widgets(*self.display.get_size())
        if self.processing:
            self.start_button.text = "Pause"


    def change_language(self):

        if type(self.language) == Default:
            self.language = Ukrainian()
        else:
            self.language = Default()

        self.init_widgets(*self.display.get_size())
        