import pygame
from time import time
from widgets import Widget
from .cell import Cell


class colors:

    background = (30, 30, 30)
    alive = (255, 255, 255)
    dead = (10, 10, 10)
    hover_alive = (150, 150, 150)
    hover_dead = (50, 50, 50)


class Field(Widget):
    
    def __init__(self, width: int, height: int, size: int, display: pygame.surface.Surface):

        super().__init__(0, 0, 0, 0)

        self.cell_size = size
        self.cols = 0
        self.rows = 0
        self.surface = pygame.surface.Surface((0, 0))
        self.window_size = (width, height)

        self.fps = 0
        self.fps_step = 3
        self.last_frame_time = time()
        self.changed_cells = []
        self.last_hover = (-1, -1)
        self.drawing_state = True
        self.pressed = False

        self.cells: list[list[Cell]] = []
        self.set_map((width+size-1) // size, (height+size-1) // size, display)
        super().__init__(0, 0, self.cols*self.cell_size, self.rows*self.cell_size)


    def set_map(self, cols, rows, display: pygame.surface.Surface):

        field = []
        nearby = [1, 2, 3, 4, 6, 7, 8, 9]
        born_conditions = [3]
        alive_conditions = [2, 3]
        if len(self.cells) > 0:
            if len(self.cells[0]) > 0:
                nearby = self.cells[0][0].nearby
                born_conditions = self.cells[0][0].born_condition
                alive_conditions = self.cells[0][0].alive_condition

        for x in range(cols):
            row: list[Cell] = []
            for y in range(rows):
                row.append(Cell(False))
                row[y].nearby = nearby
                row[y].born_condition = born_conditions
                row[y].alive_condition = alive_conditions
            field.append(row)

        start_x = (cols - self.cols + cols % 2) // 2
        start_y = (rows - self.rows + rows % 2) // 2
        for x in range(max(start_x, 0), min(start_x + self.cols, cols)):
            for y in range(max(start_y, 0), min(start_y + self.rows, rows)):
                field[x][y] = self.cells[x-start_x][y-start_y]

        self.cells = field

        self.surface = pygame.surface.Surface((cols*self.cell_size, rows*self.cell_size))
        self.rect.x -= self.cell_size * start_x
        self.rect.y -= self.cell_size * start_y
        self.rect.width = cols * self.cell_size
        self.rect.height = rows * self.cell_size

        self.cols = cols
        self.rows = rows
        for x in range(cols):
            for y in range(rows):
                self.count_nearby(x, y)
        self.resize(display)
        self.shift(0, 0)


    def set_nearby(self, nearby: list):

        for x in range(self.cols):
            for y in range(self.rows):
                cell = self.cells[x][y]
                cell.nearby = nearby
                self.count_nearby(x, y)


    def set_born(self, born_conditions: list):

        for x in range(self.cols):
            for y in range(self.rows):
                cell = self.cells[x][y]
                cell.born_condition = born_conditions


    def set_alive(self, alive_conditions: list):

        for x in range(self.cols):
            for y in range(self.rows):
                cell = self.cells[x][y]
                cell.alive_condition = alive_conditions


    def count_nearby(self, x: int, y: int):

        cell = self.cells[x][y]
        cell.neighbours = 0
        cell.neighbours_next = 0
        for n in cell.nearby:
            i = (n - 1) // 3 - 1
            j = (n - 1) % 3 - 1
            if self.cells[(x+i) % self.cols][(y+j) % self.rows].state:
                cell.neighbours += 1
                cell.neighbours_next += 1


    def edit_nearby(self, x: int, y: int, cell: Cell, change, press=False):

        for n in cell.nearby:
            i = (n - 1) // 3 - 1
            j = (n - 1) % 3 - 1
            self.cells[(x+i) % self.cols][(y+j) % self.rows].neighbours_next += change
            if press: self.cells[(x+i) % self.cols][(y+j) % self.rows].neighbours += change


    def calculate_generation(self):

        current_time = time()
        frame_time = 1 / self.fps if self.fps else 0

        if current_time - self.last_frame_time >= frame_time:
            self.last_frame_time = current_time
            self.changed_cells = []

            for x in range(self.cols):
                for y in range(self.rows):

                    cell = self.cells[x][y]
                    if not cell.state and cell.neighbours == 0: continue
                    cell.set_next_generation()
                    if cell.state != cell.state_next:
                        self.changed_cells.append([x, y])

                    change = cell.state_next - cell.state
                    if change:
                        self.edit_nearby(x, y, cell, change)


    def apply_generation(self):
        
        for x in range(self.cols):
            for y in range(self.rows):
                cell = self.cells[x][y]
                if cell.state == cell.state_next and cell.neighbours == cell.neighbours_next: continue
                cell.apply_generation()


    def draw_cell(self, x: int, y: int, color: tuple):
        
        rect = (x * self.cell_size, y * self.cell_size, self.cell_size - 1, self.cell_size - 1)
        pygame.draw.rect(self.surface, color, rect)


    def draw(self, display: pygame.surface.Surface, forced=False):
        
        if forced:
            self.surface.fill(colors.background)
            for x in range(self.cols):
                for y in range(self.rows):
                    color = colors.alive if self.cells[x][y].state else colors.dead
                    self.draw_cell(x, y, color)
        
        else:
            for c in self.changed_cells:
                x = c[0]
                y = c[1]
                cell = self.cells[x][y]
                if cell.state_previous == cell.state: continue
                color = colors.alive if self.cells[x][y].state else colors.dead
                self.draw_cell(x, y, color)

        self.changed_cells = []
        display.blit(self.surface, self.rect)


    def set_cell_state(self, x: int, y: int, state: bool):

        cell = self.cells[x][y]
        if cell.state != state:
            cell.state = state
            cell.state_next = state
            self.edit_nearby(x, y, cell, 1+(state-1)*2, press=True)


    def clear_hover(self, new_x: int, new_y: int):

        h_x, h_y = self.last_hover
        if h_x + h_y >= 0:
            color = colors.alive if self.cells[h_x][h_y].state else colors.dead
            self.draw_cell(h_x, h_y, color)
        self.last_hover = (new_x, new_y)


    def check_interaction(self, processed: bool):

        pos = list(pygame.mouse.get_pos())
        width, height = self.window_size
        
        if pos[0] <= 0 or pos[0] >= width - 1 or pos[1] <= 0 or pos[1] >= height - 1 or processed:
            x, y = (-1, -1)
        else:
            x = (pos[0] - self.rect.x) // self.cell_size
            y = (pos[1] - self.rect.y) // self.cell_size

        if pygame.mouse.get_pressed()[0] and not processed and x + y >= 0:
            if self.pressed:
                color = colors.alive if self.drawing_state else colors.dead
            else:
                self.drawing_state = not self.cells[x][y].state
                color = colors.alive if self.drawing_state else colors.dead
                self.pressed = True

            self.set_cell_state(x, y, self.drawing_state)
            self.draw_cell(x, y, color)

        else:
            self.clear_hover(x, y)

            if x + y >= 0:
                color = colors.hover_alive if self.cells[x][y].state else colors.hover_dead
                self.draw_cell(x, y, color)

            self.pressed = False
        
        return True


    def resize(self, display: pygame.surface.Surface):

        self.clear_hover(-1, -1)

        width, height = display.get_size()
        self.window_size = (width, height)

        if self.cell_size * self.cols < width:
            self.cell_size = (width + self.cols - 1) // self.cols
        if self.cell_size * self.rows < height:
            self.cell_size = (height + self.rows - 1) // self.rows

        self.surface = pygame.surface.Surface((self.cols*self.cell_size, self.rows*self.cell_size))
        self.set_rect(*self.rect.topleft, self.cols*self.cell_size, self.rows*self.cell_size)
        self.draw(display, forced=True)


    def shift(self, shift_x: int, shift_y: int):

        self.clear_hover(-1, -1)

        width, height = self.window_size
        
        self.rect.x += shift_x
        self.rect.y += shift_y
        if self.rect.x > 0: self.rect.x = 0
        elif self.rect.right < width: self.rect.right = width
        if self.rect.y > 0: self.rect.y = 0
        elif self.rect.bottom < height: self.rect.bottom = height


    def increase_cell_size(self, value: int, display: pygame.surface.Surface):

        self.clear_hover(-1, -1)

        width, height = self.window_size
        prev_cell_size = self.cell_size
        center_x = width // 2
        len_x = center_x - self.rect.x
        center_y = height // 2
        len_y = center_y - self.rect.y

        self.cell_size += value
        if self.cell_size < 2: self.cell_size = 2

        x = center_x - len_x * self.cell_size // prev_cell_size
        y = center_y - len_y * self.cell_size // prev_cell_size

        self.surface = pygame.surface.Surface((self.cols*self.cell_size, self.rows*self.cell_size))
        self.set_rect(x, y, self.cols*self.cell_size, self.rows*self.cell_size)
        self.shift(0, 0)
        self.draw(display, forced=True)


    def decrease_cell_size(self, value: int, display: pygame.surface.Surface):

        self.clear_hover(-1, -1)

        width, height = self.window_size
        prev_cell_size = self.cell_size
        center_x = width // 2
        len_x = center_x - self.rect.x
        center_y = height // 2
        len_y = center_y - self.rect.y

        self.cell_size -= value
        if self.cell_size < 2: self.cell_size = 2
        if self.cell_size * self.cols < width:
            self.cell_size = (width + self.cols - 1) // self.cols
        if self.cell_size * self.rows < height:
            self.cell_size = (height + self.rows - 1) // self.rows

        x = center_x - len_x * self.cell_size // prev_cell_size
        y = center_y - len_y * self.cell_size // prev_cell_size

        self.surface = pygame.surface.Surface((self.cols*self.cell_size, self.rows*self.cell_size))
        self.set_rect(x, y, self.cols*self.cell_size, self.rows*self.cell_size)
        self.shift(0, 0)
        self.draw(display, forced=True)
