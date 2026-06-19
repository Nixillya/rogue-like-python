import pygame
import numpy
import random
import keyboard

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True

class POS:
    x = -1
    y = -1
class PLAYER:
    pos = POS()
class MAP:
    tiles = numpy.zeros((500,500))
class MENU:
    selection = 0
class GAME:
    map = MAP()
    menu = MENU()
    play = False
    next = False

    #for x in range(0,1000,100):
    #    for y in range(0,1000,100):
    #        pygame.draw.rect(screen,"red",(x,y,100,100))

game = GAME()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # RENDER YOUR GAME HERE
    
    if game.play == False:
        screen.fill("black")
        font_size = 30
        font = pygame.font.SysFont('Comic Sans MS', font_size)

        if game.menu.selection==0:
            play_text = font.render('> PLAY', True, (255, 245, 150))
        else:
            play_text = font.render('  PLAY', True, (255, 255, 255))
        if game.menu.selection==1:
            exit_text = font.render('> EXIT', True, (255, 245, 150))
        else:
            exit_text = font.render('  EXIT', True, (255, 255, 255))

        screen.blit(play_text, ((500-font_size*2)+random.randint(-1,1),(500-font_size)+random.randint(-1,1)))
        screen.blit(exit_text, ((500-font_size*2)+random.randint(-1,1),(500+font_size)+random.randint(-1,1)))
        if(keyboard.is_pressed('w')):
            game.menu.selection = 0
        if(keyboard.is_pressed('s')):
            game.menu.selection = 1
        if(keyboard.is_pressed('enter')):
            if game.menu.selection == 1:
                running = False
            else:
                game.play = True
    else:
        screen.fill("black")

    pygame.display.flip()
    clock.tick(60)
pygame.quit()