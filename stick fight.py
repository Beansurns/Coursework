import pygame
from random import randint as rand

pygame.init()
s_width, s_height = 1900, 950
screen = pygame.display.set_mode([s_width,s_height])
g = 1

class Blocks:
    def __init__(self, width=10, height=10, pos=(1900,0), colour=(255,255,255)):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        
    def update(self):
        self.draw()
        
    def draw(self):
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.pos[0], self.pos[1], self.width, self.height))
        

class Players:
    def __init__(self, radius=10, pos=(1900, 0), colour=(255, 255, 255), xvel=0, yvel=0):
        self.radius = radius
        self.pos = pos
        self.colour = colour
        self.xvel = xvel
        self.yvel = yvel
        
    def update(self):
        self.yvel += g
        self.pos = (self.pos[0],self.pos[1]+self.yvel)
        self.draw()
    
    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.pos[0], self.pos[1]), self.radius)
    
    


players = [Players(50, (1100, 475), (2, 148, 165)), Players(50, (800, 475), (193, 64, 61))]
#TODO use tiles
blocks = [Blocks(1900, 20, (0,930), (255,255,255))]
running = True
while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    screen.fill((43, 45, 47))
    for player in players:
        player.update()
    for block in blocks:
        block.update()
    pygame.display.flip()

            
            
pygame.quit()