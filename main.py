import pygame
import sys
from game import Game


COLS = 70
ROWS = 40
SIZE = 12


pygame.init()
game = Game(COLS, ROWS, SIZE)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            game.resize()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                game.shift_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                game.shift_pressed = False


    if game.shift_pressed:

        pos = pygame.mouse.get_pos()
        size = game.display.get_size()
        shift_x = round((size[0] // 2 - pos[0]) * 8 / size[0])
        shift_y = round((size[1] // 2 - pos[1]) * 8 / size[1])

        game.field.shift(shift_x, shift_y)


    if game.processing:

        game.field.calculate_generation()
        game.field.apply_generation()

    if not game.shift_pressed:
        game.process_intereaction()
    game.draw_widgets()

    pygame.display.flip()
