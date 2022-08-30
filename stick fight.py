import pygame
from random import randint as rand

pygame.init()
#setting variables
s_width, s_height = 1900, 950
screen = pygame.display.set_mode([s_width,s_height])
g = 0.008
ydrag = 0.8
xdrag = 0.6
drag = 0.01

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
    def __init__(self, radius=10, pos=(1900, 0), colour=(255, 255, 255), num = 1, keyup = None, keydown = None, keyleft = None, keyright = None, xvel=0, yvel=0, xacc=0, yacc=0, ):
        self.radius = radius
        self.pos = pos
        self.colour = colour
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc
        self.yacc = yacc
        self.ground = False
        self.num = num
        self.keyup = keyup
        self.keydown = keydown
        self.keyleft = keyleft
        self.keyright = keyright

    def update(self):
        self.yacc += g
        self.yacc = self.yacc * ydrag
        self.yvel += self.yacc
        self.xacc = self.xacc * xdrag
        self.xvel += self.xacc
        if self.xvel > 0:
            self.xvel -= drag
        elif self.xvel < 0:
            self.xvel += drag
        else:
            None
        self.pos = (self.pos[0]+self.xvel,self.pos[1]+self.yvel)
        #Collision detection between players and surfaces
        for block in blocks:
            if (self.pos[1] + self.radius) >= block.pos[1] and (self.pos[0] > block.pos[0] and self.pos[0] < (block.pos[0] + block.width)):
                self.pos = (self.pos[0], block.pos[1]-self.radius)
                self.yvel = 0
                self.ground = True
            if (self.pos[0] + self.radius) == block.pos[1]:
                self.xvel = 0
        #movement
        keys = pygame.key.get_pressed()
        if keys[self.keyleft]:
            self.xacc += -0.01
        if keys[self.keyright]:
            self.xacc += 0.01
        if keys[self.keyup] and self.ground:
            self.yacc += -1.5
            self.ground = False
        if keys[self.keydown]:
            self.yacc += 0.01
        self.draw()
    
    def draw(self):
        #drawing the players in the game
        pygame.draw.circle(screen, self.colour, (int(self.pos[0]), int(self.pos[1])), self.radius)
        print(self.pos[0],self.pos[1])


#creating players and surfaces
players = [Players(50, (1100, 475), (2, 148, 165),num = 0,keyup = pygame.K_UP,keydown = pygame.K_DOWN,keyleft = pygame.K_LEFT, keyright = pygame.K_RIGHT)
    , Players(50, (800, 475), (193, 64, 61),num = 1,keyup = pygame.K_w,keydown = pygame.K_s,keyleft = pygame.K_a, keyright = pygame.K_d)]


blocks = [Blocks(1900, 20, (0,930), (255,255,255)), Blocks(20, 950, (0,0), (255,255,255)), Blocks(20, 950, (1880,0), (255,255,255))]
running = True
while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    screen.fill((43, 45, 47))
    for block in blocks:
        block.update()
    for player in players:
        player.update()
    pygame.display.flip()

            
            
pygame.quit()