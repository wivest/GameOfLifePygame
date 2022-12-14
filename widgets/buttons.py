from typing import Callable

import pygame

from .project_types import colors, orient, state, FONT
from . import Widget


class Button(Widget):

    def __init__(self, text: str, x: int=0, y: int=0, width: int=0, height: int=0):

        super().__init__(x, y, width, height)

        self.text = text
        self.orientation: orient
        self.update_orientation()
        self.corners = [True, True]
        self.state = state.default
        self.__callbacks: list[Callable] = []


    def update_orientation(self):

        if self.rect.width >= self.rect.height:
            self.orientation = orient.horizontal
        else:
            self.orientation = orient.vertical


    def set_orientation(self, orientation: orient):

        self.orientation = orientation

        if self.orientation == orient.horizontal and self.rect.width < self.rect.height:
            self.rect.width = self.rect.height
        elif self.orientation == orient.vertical and self.rect.width > self.rect.height:
            self.rect.height = self.rect.width


    def set_rect(self, x: int, y: int, width: int, height: int):

        super().set_rect(x, y, width, height)
        self.set_orientation(self.orientation)


    def bind(self, func: Callable):

        self.__callbacks.append(func)


    def unbind(self, func: Callable):

        self.__callbacks.remove(func)


    def draw(self, surface: pygame.surface.Surface):

        font_obj = pygame.font.SysFont(FONT, self.rect.height//3)
        text_surface = font_obj.render(self.text, True, colors.text)
        text_rect = text_surface.get_rect()

        color = colors.default
        if self.state == state.hover: color = colors.hover
        elif self.state == state.pressed: color = colors.pressed

        if self.orientation == orient.horizontal:
            size = self.rect.height // 2
            border_tl = size if self.corners[0] else -1
            border_bl = size if self.corners[0] else -1
            border_tr = size if self.corners[1] else -1
            border_br = size if self.corners[1] else -1
        else:
            size = self.rect.width // 2
            border_tl = size if self.corners[0] else -1
            border_bl = size if self.corners[1] else -1
            border_tr = size if self.corners[0] else -1
            border_br = size if self.corners[1] else -1

        pygame.draw.rect(
            surface, color, self.rect,
            border_top_left_radius=border_tl,
            border_bottom_left_radius=border_bl,
            border_top_right_radius=border_tr,
            border_bottom_right_radius=border_br
            )
        pygame.draw.rect(
            surface, colors.border, self.rect,
            border_top_left_radius=border_tl,
            border_bottom_left_radius=border_bl,
            border_top_right_radius=border_tr,
            border_bottom_right_radius=border_br,
            width=2
            )
        text_rect.center = self.rect.center
        surface.blit(text_surface, text_rect)


    def check_interaction(self, processing: bool):

        mouse = pygame.mouse

        if self.rect.collidepoint(*mouse.get_pos()) and not processing:
            processing = True
            if mouse.get_pressed()[0]:
                self.state = state.pressed
            else:
                if self.state == state.pressed:
                    for func in self.__callbacks:
                        func()
                self.state = state.hover
        else:
            self.state = state.default
        
        return processing


class TickBoxButton(Widget):

    def __init__(self, x: int=0, y: int=0, side: int=0, ticked=False):

        super().__init__(x, y, side, side)
        self.rounding = 100 # the rounding is 1 / n
        self.ticked = ticked
        self.state = state.default
        self.__callbacks: list[Callable[[bool], None]] = []


    def set_rect(self, x: int, y: int, width: int, height: int):

        size = width if height == self.rect.height else height
        super().set_rect(x, y, size, size)


    def bind(self, func: "Callable[[bool], None]"):

        self.__callbacks.append(func)


    def unbind(self, func: "Callable[[bool], None]"):

        self.__callbacks.remove(func)


    def draw(self, surface: pygame.surface.Surface):

        background_color: tuple

        if self.ticked:
            background_color = colors.tick_default_choosed
            if self.state == state.hover: background_color = colors.tick_hover_choosed
            elif self.state == state.pressed: background_color = colors.tick_pressed_choosed
        else:
            background_color = colors.tick_default
            if self.state == state.hover: background_color = colors.tick_hover
            elif self.state == state.pressed: background_color = colors.tick_pressed

        radius = self.rect.width//self.rounding
        pygame.draw.rect(surface, background_color, self.rect, border_radius=radius)
        pygame.draw.rect(surface, colors.tick_border, self.rect, width=1, border_radius=radius)


    def check_interaction(self, processing: bool):

        mouse = pygame.mouse

        if self.rect.collidepoint(*mouse.get_pos()) and not processing:
            processing = True
            if mouse.get_pressed()[0]:
                self.state = state.pressed
            else:
                if self.state == state.pressed:
                    self.ticked = not self.ticked
                    for func in self.__callbacks:
                        func(self.ticked)
                self.state = state.hover
        else:
            self.state = state.default
        
        return processing
