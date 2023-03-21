import pygame

pygame.init()

width=640
height=480

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Tic Tac Toe")

screen.fill((255,255,255))

running=True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    #update the screen
    pygame.display.flip()

pygame.quit()