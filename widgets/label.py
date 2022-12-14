import pygame
from . import Widget
from .project_types import colors, FONT


class Label(Widget):

    def __init__(self, text: str, x: int=0, y: int=0, size: int=0):

        self.text = text
        self.font = pygame.font.SysFont(FONT, size)
        super().__init__(x, y, self.font.size(self.text)[0], size)


    def set_rect(self, x: int, y: int, width: int, height: int):

        self.font = pygame.font.SysFont(FONT, height)
        super().set_rect(x, y, self.font.size(self.text)[0], height)


    def draw(self, surface: pygame.surface.Surface):
        
        text_surface = self.font.render(self.text, True, colors.text)
        surface.blit(text_surface, self.rect)
