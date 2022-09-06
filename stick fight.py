import pygame
from random import randint as rand

pygame.init()
#setting variables
s_width, s_height = 1900, 950
screen = pygame.display.set_mode([s_width,s_height])
g = 0.02
ydrag = 0.8
xdrag = 0.5
drag = 0.6
xvdrag = 0.1/0.13

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

class Borders:
    def __init__(self, width=10, height=1, pos=(1900, 0), vert=True, tr=True):
        self.width = width
        self.height = height
        self.pos = pos
        self.vert = vert
        self.tr = tr

    def update(self):
        self.draw()

    def draw(self):
        pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        

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
        self.xvel = self.xvel * xvdrag


        self.pos = (self.pos[0]+self.xvel,self.pos[1]+self.yvel)
        #Collision detection between players and surfaces
        for border in borders:
            if border.vert == False and border.tr == True and (self.pos[1] + self.radius) >= border.pos[1] and (self.pos[0] > border.pos[0] and self.pos[0] < (border.pos[0] + border.width)):
                self.pos = (self.pos[0], border.pos[1]-self.radius)
                self.yvel = 0
                self.ground = True
            elif border.vert == True and border.tr == True and -1 < ((self.pos[0] - self.radius) - border.pos[0]) < 1 and (self.pos[1] > border.pos[1] and self.pos[1] < (border.pos[1] + border.height)):
                self.xvel = 0
                self.pos = (border.pos[0] + border.width + self.radius, self.pos[1])
            elif border.vert == True and border.tr == False and -1 < ((self.pos[0] + self.radius) - border.pos[0]) < 1 and (self.pos[1] > border.pos[1] and self.pos[1] < (border.pos[1] + border.height)):
                self.xvel = 0
                self.pos = (border.pos[0] - border.width - self.radius, self.pos[1])

        #movement
        keys = pygame.key.get_pressed()
        if keys[self.keyleft]:
            self.xacc += -0.8
        if keys[self.keyright]:
            self.xacc += 0.8
        if keys[self.keyup] and self.ground:
            self.yacc += -1.3
            self.ground = False
        if keys[self.keydown]:
            self.yacc += 0.3
        self.draw()
    
    def draw(self):
        #drawing the players in the game
        pygame.draw.circle(screen, self.colour, (int(self.pos[0]), int(self.pos[1])-1), self.radius)


#creating players and surfaces
players = [Players(30, (1100, 475), (2, 148, 165),num = 0,keyup = pygame.K_UP,keydown = pygame.K_DOWN,keyleft = pygame.K_LEFT, keyright = pygame.K_RIGHT)
    , Players(30, (800, 475), (193, 64, 61),num = 1,keyup = pygame.K_w,keydown = pygame.K_s,keyleft = pygame.K_a, keyright = pygame.K_d)]


blocks = [Blocks(1900, 20, (0,930), (255,255,255)), Blocks(20, 950, (0,0), (255,255,255)), Blocks(20, 950, (1880,0), (255,255,255)), Blocks(800, 20, (550,630), (255,255,255))]

borders = [Borders(1900,1,(0,931), False, True), Borders(1, 950, (19,0), True, True),
           Borders(1, 950, (1880,0), True, False), Borders(800,1,(550,631), False, True),
           Borders(1, 20, (1349,630), True, True), Borders(1, 20, (550,630), True, False),
           Borders(800,1,(550,670), False, False)]
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