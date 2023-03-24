import pygame
import time as t
import os 
import numpy as np
from sprites_module import Xspot, Ospot, Restart_Button

# Setting up pygame Window
pygame.init()
clock=pygame.time.Clock()
screen_width=600
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Tic Tac Toe")

# Setting up sprite Groups
sprite_group=pygame.sprite.Group()
reset_group=pygame.sprite.Group()

def startGame():
    # Defining game over boolean
    GameOver=(False, None)
    #Set Sprite Group object to add X and O s to
    sprite_group.empty()
    reset_group.empty()
    # setting tic tac toe background
    background=pygame.image.load(os.path.join("sprite","Background.png"))
    background=pygame.transform.scale(background,(screen_height,screen_width))
    # Render background
    screen.fill((255,255,255))
    screen.blit(background,(0,0))
    
    # Setting Game Tracking Matrix used for understanding who wins and if a spot is taken
    # X is a 1 and O is a 0 no value is -1
    record=[[-1],[-1],[-1],
            [-1],[-1],[-1],
            [-1],[-1],[-1]]

    return GameOver, record, sprite_group, reset_group


# Function to check of the mouse click is within a specified region
def box_check(mouse_pos,box):
    # Checking 
    if (mouse_pos[0]>box[0]) and (mouse_pos[0]<box[1]):
        # Checking Y
        if (mouse_pos[1]>box[2]) and (mouse_pos[1]<box[3]):
            check=True
        else: 
            check =False
    else: 
        check=False
    return check

# Function that marks the spot on the screen
def mark_spot(turn,pos):
    # Place X or O on screen depending whose turn it is
        if turn:
            xspot=Xspot(pos)
            sprite_group.add(xspot)
        else:
            ospot=Ospot(pos)
            sprite_group.add(ospot)

def isGameOver(record):
    isFinished=False
    isWinner=None
    def winner(a):
        if a==1:
            out='X'
        else:
            out='O'
        return out

    matrix_record=np.array(record)
    matrix_record=matrix_record.reshape(3,3)
    print(f'Record in Matrix Form:\n{matrix_record}')

    #Start loop checking 3 spots for winner
    for i in range(0,3):

        # Check Rows for Win, have to account for at the start of the game all rows and columns match with -1
        if (matrix_record[i,0]==matrix_record[i,1]) and (matrix_record[i,0]==matrix_record[i,2]) and (matrix_record[i,0]!=-1):
            isFinished=True
            isWinner=winner(matrix_record[i,0])

        # Check Columns for win
        if (matrix_record[0,i]==matrix_record[1,i]) and (matrix_record[0,i]==matrix_record[2,i])and (matrix_record[0,i]!=-1):
            isFinished=True
            isWinner=winner(matrix_record[0,i])

    #Check Diagonals
    if (matrix_record[0,0]==matrix_record[1,1]) and (matrix_record[0,0]==matrix_record[2,2])and (matrix_record[0,0]!=-1):
        isFinished=True
        isWinner=winner(matrix_record[0,0])
    elif (matrix_record[0,2]==matrix_record[1,1]) and (matrix_record[0,2]==matrix_record[2,0])and (matrix_record[0,2]!=-1):
        isFinished=True
        isWinner=winner(matrix_record[0,2])

    # Is all squares are taken the game is over and there is no winner
    if -1 not in np.array(record).reshape(1,9)[0]:
        isFinished=True
        isWinner='Tie'
            
    return (isFinished, isWinner)

class Single_Mouse_Click():
    def __init__(self):
        self.pressedDown=False
        self.singleClick=False
    def check(self):
        if event.type==pygame.MOUSEBUTTONDOWN:
            self.pressedDown=True
        elif (self.pressedDown==True) and (pygame.mouse.get_pressed()[0]==False):
            self.singleClick=True
            self.pressedDown=False
        # Reset single button click if it was pressed
        elif self.singleClick==True:
            self.singleClick=False
        return self.singleClick
# Defining coordinates for each space on board
#[minX,maxX,minY,maxY],[minX,maxX,minY,maxY],[minX,maxX,minY,maxY]
#[minX,maxX,minY,maxY],[minX,maxX,minY,maxY],[minX,maxX,minY,maxY]
#[minX,maxX,minY,maxY],[minX,maxX,minY,maxY],[minX,maxX,minY,maxY]

game_cord=[[0,200,0,200],[200,400,0,200],[400,600,0,200],
            [0,200,200,400],[200,400,200,400],[400,600,200,400],
            [0,200,400,600],[200,400,400,600],[400,600,400,600]]

sprite_render_cord=[[100,100],[300,100],[500,100],
                    [100,300],[300,300],[500,300],
                    [100,500],[300,500],[500,500]]


print('Enter Game Loop')
isXturn=True
running=True
GameOver, record, sprite_group, reset_group=startGame()
restart_button=Restart_Button(startGame)
single_mouse_click=Single_Mouse_Click()
while running:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    # Click event on the screen
    playerEvent=False
    if single_mouse_click.check():
        print('*******************')
        print(pygame.mouse.get_pressed())
        # Grab Mouse Position
        mouse_pos=pygame.mouse.get_pos()
        print(mouse_pos)

        for i in range(0,len(game_cord)):
            check=box_check(mouse_pos,game_cord[i])
            if check:
                playerEvent=True
                # Check to see if the spot was already in use.
                if record[i][0]==-1:
                    mark_spot(isXturn,sprite_render_cord[i])

                    # Record that the spot is taken and if it is an X or an O
                    if isXturn:
                        record[i][0]=1
                    else:
                        record[i][0]=0

                    # Change Turns
                    isXturn=not isXturn

    # Checking to see if the game is over
    GameOver=isGameOver(record)
    if (GameOver[0]) and (playerEvent==False):
        print(f'Winner is {GameOver[1]}')
        reset_group.add(restart_button)
        t.sleep(1)    

    reset_group.update()
    reset_group.draw(screen)
    sprite_group.draw(screen)
        
    #update the screen
    pygame.display.flip()
    clock.tick(60)


pygame.quit()