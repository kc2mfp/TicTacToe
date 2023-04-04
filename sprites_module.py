import pygame
import os

# Creating X Sprite
class Xspot(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image=pygame.image.load(os.path.join("sprite","X.png"))
        self.rect=self.image.get_rect()
        self.rect.center=[pos[0],pos[1]]
        
# Creating O Sprite
class Ospot(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image=pygame.image.load(os.path.join("sprite","O.png"))
        self.rect=self.image.get_rect()
        self.rect.center=[pos[0],pos[1]]

# Restart Button Displayed after someone wins the game
class Restart_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(os.path.join('sprite','Reset.png'))
        self.rect=self.image.get_rect()
        self.rect.center=[300,300]
