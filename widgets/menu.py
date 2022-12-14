import pygame
from . import Widget, BoxLayoutV, BoxLayoutH, Button, Label, TickBoxButton
from .project_types import colors, FONT_SIZE
from .field import Field
from .language_pack import Default


class Menu(Widget):

    def __init__(self, field: Field, x: int, y: int, height: int, button_size: int, display: pygame.surface.Surface, language: Default):

        indent = 10
        width = 200 + 2*indent
        super().__init__(x, y, width, height)
        self.display = display
        self.field = field
        self.language = language
        self.layout = BoxLayoutV(x + indent, y + indent + button_size + indent, width - 2*indent)
        self.opened = False
        self.menu_button = Button(self.language.OPEN_MENU_BUTTON, indent, indent, button_size*3//2, button_size)
        self.menu_button.bind(self.activate_menu)


        self.ticks_nearby: list[TickBoxButton] = []
        for i in range(9):
            tick_button = TickBoxButton(ticked=True)
            tick_button.bind(self.tick_cell_nearby)
            self.ticks_nearby.append(tick_button)
        self.ticks_nearby[4].ticked = False

        label = Label(self.language.NEARBY_CELLS_MAP_LABEL, size=FONT_SIZE)
        empty_horizontal = Widget(height=indent//2)
        empty = Widget(width=indent//2)
        self.layout.add_widget(label)
        row = BoxLayoutH(height=30)
        row.add_widgets(self.ticks_nearby[8], empty, self.ticks_nearby[5], empty, self.ticks_nearby[2])
        self.layout.add_widgets(empty_horizontal, row)
        row = BoxLayoutH(height=30)
        row.add_widgets(self.ticks_nearby[7], empty, self.ticks_nearby[4], empty, self.ticks_nearby[1])
        self.layout.add_widgets(empty_horizontal, row)
        row = BoxLayoutH(height=30)
        row.add_widgets(self.ticks_nearby[6], empty, self.ticks_nearby[3], empty, self.ticks_nearby[0])
        self.layout.add_widgets(empty_horizontal, row, empty_horizontal, empty_horizontal)


        self.ticks_birth: list[TickBoxButton] = []
        for i in range(9):
            tick_button = TickBoxButton()
            tick_button.bind(self.tick_cell_birth)
            self.ticks_birth.append(tick_button)
        self.ticks_birth[2].ticked = True

        label = Label(self.language.BIRTH_CONDITIONS_LABEL, size=FONT_SIZE)
        self.layout.add_widgets(label, empty_horizontal)
        empty = Widget(width=10)
        row = BoxLayoutH(height=15)
        row.add_widgets(
            Label("1: ", size=FONT_SIZE), self.ticks_birth[0], empty,
            Label("2: ", size=FONT_SIZE), self.ticks_birth[1], empty,
            Label("3: ", size=FONT_SIZE), self.ticks_birth[2], empty,
            Label("4: ", size=FONT_SIZE), self.ticks_birth[3], empty,
            Label("5: ", size=FONT_SIZE), self.ticks_birth[4]
            )
        self.layout.add_widgets(row, empty_horizontal)
        row = BoxLayoutH(height=15)
        row.add_widgets(
            Label("6: ", size=FONT_SIZE), self.ticks_birth[5], empty,
            Label("7: ", size=FONT_SIZE), self.ticks_birth[6], empty,
            Label("8: ", size=FONT_SIZE), self.ticks_birth[7], empty,
            Label("9: ", size=FONT_SIZE), self.ticks_birth[8]
            )
        self.layout.add_widgets(row, empty_horizontal, empty_horizontal)


        self.ticks_alive: list[TickBoxButton] = []
        for i in range(10):
            tick_button = TickBoxButton()
            tick_button.bind(self.tick_cell_alive)
            self.ticks_alive.append(tick_button)
        self.ticks_alive[2].ticked = True
        self.ticks_alive[3].ticked = True

        label = Label(self.language.ALIVE_CONDITIONS_LABEL, size=FONT_SIZE)
        self.layout.add_widgets(label, empty_horizontal)
        empty = Widget(width=10)
        row = BoxLayoutH(height=15)
        row.add_widgets(
            Label("0: ", size=FONT_SIZE), self.ticks_alive[0], empty,
            Label("1: ", size=FONT_SIZE), self.ticks_alive[1], empty,
            Label("2: ", size=FONT_SIZE), self.ticks_alive[2], empty,
            Label("3: ", size=FONT_SIZE), self.ticks_alive[3], empty,
            Label("4: ", size=FONT_SIZE), self.ticks_alive[4]
            )
        self.layout.add_widgets(row, empty_horizontal)
        row = BoxLayoutH(height=15)
        row.add_widgets(
            Label("5: ", size=FONT_SIZE), self.ticks_alive[5], empty,
            Label("6: ", size=FONT_SIZE), self.ticks_alive[6], empty,
            Label("7: ", size=FONT_SIZE), self.ticks_alive[7], empty,
            Label("8: ", size=FONT_SIZE), self.ticks_alive[8], empty,
            Label("9: ", size=FONT_SIZE), self.ticks_alive[9]
            )
        self.layout.add_widgets(row, empty_horizontal)

        increase_cols = Button(self.language.INCREASE_COLUMNS_BUTTON, width=button_size*2)
        increase_cols.bind(self.increase_cols)
        decrease_cols = Button(self.language.DECREASE_COLUMNS_BUTTON, width=button_size*2)
        decrease_cols.bind(self.decrease_cols)
        cols_layout = BoxLayoutH(height=button_size)
        cols_layout.add_widgets(increase_cols, empty, decrease_cols)
        self.layout.add_widget(cols_layout)
        self.cols_label = Label(f"{self.language.CURRENT_COLUMNS_LABEL}{self.field.cols}", size=FONT_SIZE)
        self.layout.add_widgets(self.cols_label, empty_horizontal)

        increase_rows = Button(self.language.INCREASE_ROWS_BUTTON, width=button_size*2)
        increase_rows.bind(self.increase_rows)
        decrease_rows = Button(self.language.DECREASE_ROWS_BUTTON, width=button_size*2)
        decrease_rows.bind(self.decrease_rows)
        rows_layout = BoxLayoutH(height=button_size)
        rows_layout.add_widgets(increase_rows, empty, decrease_rows)
        self.layout.add_widget(rows_layout)
        self.rows_label = Label(f"{self.language.CURRENT_ROWS_LABEL}{self.field.rows}", size=FONT_SIZE)
        self.layout.add_widgets(self.rows_label, empty_horizontal)


    def tick_cell_nearby(self, ticked: bool):

        nearby = []
        for i in range(1, 10):
            if self.ticks_nearby[i-1].ticked:
                nearby.append(i)
        self.field.set_nearby(nearby)


    def tick_cell_birth(self, ticked: bool):

        born_conditions = []
        for i in range(1, 10):
            if self.ticks_birth[i-1].ticked:
                born_conditions.append(i)
        self.field.set_born(born_conditions)


    def tick_cell_alive(self, ticked: bool):

        alive_conditions = []
        for i in range(0, 10):
            if self.ticks_alive[i].ticked:
                alive_conditions.append(i)
        self.field.set_alive(alive_conditions)


    def increase_cols(self):

        self.field.set_map(self.field.cols + 1, self.field.rows, self.display)
        self.cols_label.text = f"{self.language.CURRENT_COLUMNS_LABEL}{self.field.cols}"


    def decrease_cols(self):

        self.field.set_map(max(self.field.cols - 1, 1), self.field.rows, self.display)
        self.cols_label.text = f"{self.language.CURRENT_COLUMNS_LABEL}{self.field.cols}"


    def increase_rows(self):

        self.field.set_map(self.field.cols, self.field.rows + 1, self.display)
        self.rows_label.text = f"{self.language.CURRENT_ROWS_LABEL}{self.field.rows}"


    def decrease_rows(self):

        self.field.set_map(self.field.cols, max(self.field.rows - 1, 1), self.display)
        self.rows_label.text = f"{self.language.CURRENT_ROWS_LABEL}{self.field.rows}"


    def activate_menu(self):

        self.opened = not self.opened
        if self.opened:
            self.menu_button.text = self.language.OPEN_MENU_BUTTON_CLOSE
        else:
            self.menu_button.text = self.language.OPEN_MENU_BUTTON


    def add_widget(self, widget: Widget):

        self.layout.add_widget(widget)


    def draw(self, surface: pygame.surface.Surface):
        
        if self.opened:
            pygame.draw.rect(surface, colors.menu_background, self.rect)
            self.layout.draw(surface)
        self.menu_button.draw(surface)

    
    def check_interaction(self, processing: bool):
        
        processing = self.menu_button.check_interaction(processing)
        
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.opened:
            self.layout.check_interaction(processing)
            processing = True

        return processing
