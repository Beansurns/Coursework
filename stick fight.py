import pygame
from random import randint as rand

pygame.init()
#setting variables
s_width, s_height = 1900, 950
screen = pygame.display.set_mode([s_width,s_height])
g = 0.02

class Blocks:
    def __init__(self, width=10, height=10, pos=(1900,0), colour=(255,255,255)):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        
    def update(self):
        self.draw()
        
    def draw(self):
        #drawing the surfaces in the game
        pygame.draw.rect(screen, self.colour, pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.width, self.height))
        

class Players:
    def __init__(self, radius=10, pos=(1900, 0), colour=(255, 255, 255), xvel=0, yvel=0):
        self.radius = radius
        self.pos = pos
        self.colour = colour
        self.xvel = xvel
        self.yvel = yvel
        
    def update(self):
        self.yvel += g
        self.pos = (self.pos[0]+self.xvel,self.pos[1]+self.yvel)
        #Collision detection between players and surfaces
        for block in blocks:
            if (self.pos[1] + self.radius) >= block.pos[1]:
                self.pos = (self.pos[0], block.pos[1]-self.radius)
                self.yvel = 0
        self.draw()
    
    def draw(self):
        #drawing the players in the game
        pygame.draw.circle(screen, self.colour, (int(self.pos[0]), int(self.pos[1])), self.radius)
    

#TODO keybind movement



#creating players and surfaces
players = [Players(50, (1100, 475), (2, 148, 165)), Players(50, (800, 475), (193, 64, 61))]
#TODO use tiles
blocks = [Blocks(1900, 20, (0,930), (255,255,255))]
running = True
while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    #checking for key presses and implementing the actions accordingly
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        players[1].xvel = players[1].xvel - 0.1
    if keys[pygame.K_RIGHT]:
        players[1].xvel = players[1].xvel + 0.1
    if keys[pygame.K_UP]:
        players[1].yvel = players[1].yvel - 0.1
    if keys[pygame.K_DOWN]:
        players[1].yvel = players[1].yvel + 0.1

    if keys[pygame.K_a]:
        players[0].xvel = players[0].xvel - 0.1
    if keys[pygame.K_d]:
        players[0].xvel = players[0].xvel + 0.1
    if keys[pygame.K_w]:
        players[0].yvel = players[0].yvel - 0.1
    if keys[pygame.K_s]:
        players[0].yvel = players[0].yvel + 0.1

    screen.fill((43, 45, 47))
    for player in players:
        player.update()
    for block in blocks:
        block.update()
    pygame.display.flip()

            
            
pygame.quit()