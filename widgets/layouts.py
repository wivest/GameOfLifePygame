import pygame
from . import Widget


class BoxLayoutH(Widget):

    def __init__(self, x: int=0, y: int=0, height: int=0):

        super().__init__(x, y, 0, height)
        self.widgets: list[Widget] = []


    def set_rect(self, x: int, y: int, width: int, height: int):
        
        super().set_rect(x, y, width, height)
        cur_x = self.rect.x
        for widget in self.widgets:
            widget.set_rect(cur_x, y, widget.rect.width, self.rect.height)
            cur_x += widget.rect.width


    def add_widget(self, widget: Widget):

        x = self.rect.right - 1
        y = self.rect.y
        widget.set_rect(x, y, widget.rect.width, self.rect.height)
        self.widgets.append(widget)
        self.rect.width += widget.rect.width


    def add_widgets(self, *widgets: Widget):

        for widget in widgets:
            self.add_widget(widget)


    def draw(self, surface: pygame.surface.Surface):
        
        for widget in self.widgets:
            widget.draw(surface)


    def check_interaction(self, processing: bool):
        
        for widget in self.widgets:
            processing = widget.check_interaction(processing)

        return processing


class BoxLayoutV(Widget):

    def __init__(self, x: int=0, y: int=0, width: int=0):

        super().__init__(x, y, width, 0)
        self.widgets: list[Widget] = []


    def set_rect(self, x: int, y: int, width: int, height: int):
        
        super().set_rect(x, y, width, height)
        cur_y = self.rect.y
        for widget in self.widgets:
            widget.set_rect(x, cur_y, self.rect.width, widget.rect.height)
            cur_y += widget.rect.height


    def add_widget(self, widget: Widget):

        x = self.rect.x
        y = self.rect.bottom - 1
        widget.set_rect(x, y, self.rect.width, widget.rect.height)
        self.widgets.append(widget)
        self.rect.height += widget.rect.height


    def add_widgets(self, *widgets: Widget):

        for widget in widgets:
            self.add_widget(widget)


    def draw(self, surface: pygame.surface.Surface):
        
        for widget in self.widgets:
            widget.draw(surface)


    def check_interaction(self, processing: bool):
        
        for widget in self.widgets:
            processing = widget.check_interaction(processing)

        return processing
