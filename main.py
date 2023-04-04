import pygame
import time as t
import os 
import numpy as np
from sprites_module import Xspot, Ospot, Restart_Button

class gameDisplay():
    def __init__(self):
        # Setting up pygame Window
        pygame.init()
        self.screen_width=600
        self.screen_height=600
        self.screen=pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")

        # Setting up sprite Groups
        self.sprite_group=pygame.sprite.Group()

        # Setting Game Tracking Matrix used for understanding who wins and if a spot is taken
        # X is a 1 and O is a 0 no value is -1
        self.record=[[-1],[-1],[-1],
                [-1],[-1],[-1],
                [-1],[-1],[-1]]
    
        self.isGameOver=False
        self.winnerIs=None

    def startGame(self):
        # setting tic tac toe background
        background=pygame.image.load(os.path.join("sprite","Background.png"))
        background=pygame.transform.scale(background,(self.screen_height,self.screen_width))
        # Render background
        self.screen.fill((255,255,255))
        self.screen.blit(background,(0,0))

    # Function to check of the mouse click is within a specified region
    def box_check(self,mouse_pos,box):
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
    def mark_spot(self,turn,pos):
        # Place X or O on screen depending whose turn it is
            if turn:
                xspot=Xspot(pos)
                self.sprite_group.add(xspot)
            else:
                ospot=Ospot(pos)
                self.sprite_group.add(ospot)

    def gameOverCheck(self):

        def winner(a):
            if a==1:
                out='X'
            else:
                out='O'
            return out

        matrix_record=np.array(self.record)
        matrix_record=matrix_record.reshape(3,3)
        #print(f'Record in Matrix Form:\n{matrix_record}')

        #Start loop checking 3 spots for winner
        for i in range(0,3):

            # Check Rows for Win, have to account for at the start of the game all rows and columns match with -1
            if (matrix_record[i,0]==matrix_record[i,1]) and (matrix_record[i,0]==matrix_record[i,2]) and (matrix_record[i,0]!=-1):
                self.isGameOver=True
                self.winnerIs=winner(matrix_record[i,0])

            # Check Columns for win
            if (matrix_record[0,i]==matrix_record[1,i]) and (matrix_record[0,i]==matrix_record[2,i])and (matrix_record[0,i]!=-1):
                self.isGameOver=True
                self.winnerIs=winner(matrix_record[0,i])

        #Check Diagonals
        if (matrix_record[0,0]==matrix_record[1,1]) and (matrix_record[0,0]==matrix_record[2,2])and (matrix_record[0,0]!=-1):
            self.isGameOver=True
            self.winnerIs=winner(matrix_record[0,0])
        elif (matrix_record[0,2]==matrix_record[1,1]) and (matrix_record[0,2]==matrix_record[2,0])and (matrix_record[0,2]!=-1):
            self.isGameOver=True
            self.winnerIs=winner(matrix_record[0,2])

        # Is all squares are taken the game is over and there is no winner
        if -1 not in np.array(self.record).reshape(1,9)[0]:
            self.isGameOver=True
            self.winnerIs='Tie'
    
    def draw(self):
        self.sprite_group.draw(self.screen)
                

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
clock=pygame.time.Clock()
isXturn=True
running=True
gameDis=gameDisplay()
gameDis.startGame()
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

        if gameDis.isGameOver:
            del gameDis
            gameDis=gameDisplay()
            gameDis.startGame()
            continue

        for i in range(0,len(game_cord)):
            check=gameDis.box_check(mouse_pos,game_cord[i])
            if check:
                playerEvent=True
                # Check to see if the spot was already in use.
                if gameDis.record[i][0]==-1:
                    gameDis.mark_spot(isXturn,sprite_render_cord[i])

                    # Record that the spot is taken and if it is an X or an O
                    if isXturn:
                        gameDis.record[i][0]=1
                    else:
                        gameDis.record[i][0]=0

                    # Change Turns
                    isXturn=not isXturn

    # Checking to see if the game is over
    gameDis.gameOverCheck()
    if (gameDis.isGameOver) and (playerEvent==False):
        #print(f'Winner is {gameDis.winnerIs}')
        restbutton=Restart_Button()
        gameDis.sprite_group.add(restbutton)

    
    gameDis.draw()
        
    #update the screen
    pygame.display.flip()
    clock.tick(60)


pygame.quit()