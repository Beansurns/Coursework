import pygame
from random import randint as rand

pygame.init()
s_width, s_height = 1900, 950
screen = pygame.display.set_mode([s_width,s_height])

class Blocks:
    def __init__(self, width=10, height=10, pos=(1900,0), colour=(255,255,255)):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        
    def update(self):
        
        self.draw()
        
    def draw(self):
        pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        

class Players:
    def __init__(self, width=10, height=20, pos=(1900, 0), colour=(255, 255, 255)):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        
    def update(self):
        pass
    
    def draw(self):
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.pos[0], self.pos[1], self.width, self.height))
    
    


players = []

running = True
while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((43, 45, 47))
    pygame.display.flip()

            
            
pygame.quit()