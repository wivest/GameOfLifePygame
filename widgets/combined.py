import pygame
from . import Widget
from . import Button
from .project_types import orient, colors


class CombinedButtonsH(Widget):

    def __init__(self, x: int=0, y: int=0, height: int=0):

        super().__init__(x, y, 0, height)
        self.splitter_padding = height // 6
        self.buttons: list[Button] = []


    def set_rect(self, x: int, y: int, width: int, height: int):

        super().set_rect(x, y, width, height)
        self.splitter_padding = self.rect.height // 6
        current_x = x
        self.rect.width = 0
        for button in self.buttons:
            button.set_rect(current_x, y, button.rect.width, height)
            self.rect.width += button.rect.width
            current_x += button.rect.width


    def add_button(self, button: Button):

        button.rect.height = self.rect.height
        button.rect.y = self.rect.y
        button.rect.x = self.rect.right - 1
        button.set_orientation(orient.horizontal)

        amount = len(self.buttons)
        self.rect.width += button.rect.width

        if amount > 0:
            button.corners[0] = False
            self.buttons[amount-1].corners[1] = False
        self.buttons.append(button)


    def add_buttons(self, *buttons: Button):

        for button in buttons:
            self.add_button(button)


    def draw(self, surface: pygame.surface.Surface):

        for button in self.buttons:
            button.draw(surface)

            if not button.corners[0]:
                top = list(button.rect.topleft)
                bottom = list(button.rect.bottomleft)
                top[1] += self.splitter_padding
                bottom[1] -= self.splitter_padding + 1
                
                pygame.draw.line(surface, colors.splitter, top, bottom)

            if not button.corners[1]:
                top = list(button.rect.topright)
                bottom = list(button.rect.bottomright)
                top[0] -= 1
                top[1] += self.splitter_padding
                bottom[0] -= 1
                bottom[1] -= self.splitter_padding + 1
                
                pygame.draw.line(surface, colors.splitter, top, bottom)


    def check_interaction(self, processed: bool):

        for button in self.buttons:
            processed = button.check_interaction(processed)
        
        return processed
