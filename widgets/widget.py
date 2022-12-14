import pygame


class Widget:

    def __init__(self, x: int=0, y: int=0, width: int=0, height: int=0):

        self.rect = pygame.Rect(x, y, width, height)


    def set_rect(self, x: int, y: int, width: int, height: int):

        self.rect = pygame.Rect(x, y, width, height)


    def draw(self, surface: pygame.surface.Surface):

        pass

    
    def check_interaction(self, processing: bool):
        
        return processing
