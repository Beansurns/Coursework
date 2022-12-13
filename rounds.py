import pygame
import time
from random import randint as rand

pygame.init()
#setting variables
s_width, s_height = 1900, 950
screen = pygame.display.set_mode([s_width,s_height])
g = 9800
ydrag = 0.8
xdrag = 0.5
drag = 0.6
xvdrag = 0.1/0.13
clock = pygame.time.Clock()

class Blocks:
    def __init__(self, width=10, height=10, pos=(1900,0), colour=(255,255,255)):
        self.width = width
        self.height = height
        self.pos = pos
        self.colour = colour
        
    def update(self, dt):
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
    def __init__(self, radius=10, pos=(1900, 0), colour=(255, 255, 255), num = 1, keyup = None, keydown = None,
                 keyleft = None, keyright = None,pl = 0,bullets = 10, xvel=0, yvel=0, xacc=0, yacc=0, last_jump = 0, health = 500):
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
        self.last_jump = last_jump
        self.pl = pl
        self.bullets = bullets
        self.health = health

    def update(self, dt):
        self.ground = False
        self.yacc = self.yacc * ydrag
        self.yvel += (self.yacc + g)*dt
        self.xacc = self.xacc * xdrag
        self.xvel += self.xacc*dt
        self.xvel = self.xvel * xvdrag
        if self.health <= 0:
            self.pos = (950,475)
            self.health = 500


        self.pos = (self.pos[0]+(self.xvel * dt), self.pos[1]+(self.yvel * dt))
        #Collision detection between players and surfaces
        for border in borders:
            if border.pos[1] == 931 and -1 < (self.pos[1] + self.radius) - border.pos[1]:
                self.pos = (self.pos[0], border.pos[1] - self.radius)
                self.yvel = 0
                self.ground = True
            elif not border.vert and border.tr and -1 < (self.pos[1] + self.radius) - border.pos[1] < 10 and \
                    (self.pos[0] > border.pos[0] and self.pos[0] < (border.pos[0] + border.width)):
                self.pos = (self.pos[0], border.pos[1]-self.radius)
                self.yvel = 0
                self.ground = True
            elif border.vert and border.tr and -5 < ((self.pos[0] - self.radius) - border.pos[0]) < 1 \
                    and (self.pos[1] > border.pos[1] and self.pos[1] < (border.pos[1] + border.height)):
                self.xvel = 0
                self.pos = (border.pos[0] + border.width + self.radius, self.pos[1])
            elif border.vert and not border.tr and -1 < ((self.pos[0] + self.radius) - border.pos[0]) < 5 \
                    and (self.pos[1] > border.pos[1] and self.pos[1] < (border.pos[1] + border.height)):
                self.xvel = 0
                self.pos = (border.pos[0] - border.width - self.radius, self.pos[1])
            elif not border.vert and not border.tr and -10 < (self.pos[1] - self.radius) - border.pos[1] < 1 and \
                    (self.pos[0] > border.pos[0] and self.pos[0] < (border.pos[0] + border.width)):
                self.pos = (self.pos[0], border.pos[1] + self.radius + border.height)
                self.yvel = 0

        #movement
        keys = pygame.key.get_pressed()
        if keys[self.keyleft]:
            self.xacc += -100000
        if keys[self.keyright]:
            self.xacc += 100000
        if keys[self.keyup] and self.ground:
            self.yvel += -3000
            self.ground = False
        if keys[self.keydown]:
            self.yacc += 10000
        self.draw()
    
    def draw(self):
        #drawing the players in the game
        pygame.draw.circle(screen, self.colour, (int(self.pos[0]), int(self.pos[1])-1), self.radius)

class Bullet:
    def __init__(self, pl, xdir, ydir, bounces = 0, bounce_potential = 0, dmg = 10, radius = 10, xvel = 10, yvel = 10):
        self.pl = pl
        self.xdir = xdir
        self.ydir = ydir
        self.pos = (players[pl].pos[0],players[pl].pos[1])
        self.bounces = bounces
        self.bounce_potential = bounce_potential
        self.dmg = dmg
        self.radius = radius
        self.xvel = xvel
        self.yvel = yvel

    def update(self, dt):
        self.yvel += g/1000
        self.pos = (self.pos[0] + self.xvel*dt, self.pos[1] + self.yvel*dt)
        for border in borders:
            if border.pos[1] == 931 and -1 < (self.pos[1] + self.radius) - border.pos[1]:
                self.bounces += 1
                self.yvel *= -1
            elif not border.vert and border.tr and -1 < (self.pos[1] + self.radius) - border.pos[1] < 10 and \
                    (self.pos[0] > border.pos[0] and self.pos[0] < (border.pos[0] + border.width)):
                self.bounces += 1
                self.yvel *= -1
            elif border.vert and border.tr and -5 < ((self.pos[0] - self.radius) - border.pos[0]) < 1 \
                    and (self.pos[1] > border.pos[1] and self.pos[1] < (border.pos[1] + border.height)):
                self.bounces += 1
                self.xvel *= -1
            elif border.vert and not border.tr and -1 < ((self.pos[0] + self.radius) - border.pos[0]) < 5 \
                    and (self.pos[1] > border.pos[1] and self.pos[1] < (border.pos[1] + border.height)):
                self.bounces += 1
                self.xvel *= -1
            elif not border.vert and not border.tr and -10 < (self.pos[1] - self.radius) - border.pos[1] < 1 and \
                    (self.pos[0] > border.pos[0] and self.pos[0] < (border.pos[0] + border.width)):
                self.bounces += 1
                self.yvel *= -1
        for player in players:
            if (self.pos[0]-player.pos[0])**2+(self.pos[1]-player.pos[1])**2 <= (self.radius+player.radius)**2 and self.pl != player.pl:
                self.bounces = self.bounce_potential + 1
                player.health -= 10
        self.draw()

    def draw(self):
        pygame.draw.circle(screen, (255,255,255), (int(self.pos[0]), int(self.pos[1])), self.radius)


#creating players and surfaces
players = [Players(30, (1100, 475), (2, 148, 165),num = 0,keyup = pygame.K_UP,keydown = pygame.K_DOWN,
                   keyleft = pygame.K_LEFT, keyright = pygame.K_RIGHT, pl = 0, bullets = 10)
    , Players(30, (800, 475), (193, 64, 61),num = 1,keyup = pygame.K_w,keydown = pygame.K_s,keyleft = pygame.K_a,
              keyright = pygame.K_d, pl = 1, bullets = 10)]


blocks = [Blocks(1900, 20, (0,930), (255,255,255)), Blocks(20, 950, (0,0), (255,255,255)), Blocks(20, 950, (1880,0),
                (255,255,255)), Blocks(800, 20, (550,630), (255,255,255)), Blocks(400, 20, (750,330), (255,255,255))]

borders = [Borders(1900, 1, (0, 931), False, True), Borders(1, 950, (19, 0), True, True),
           Borders(1, 950, (1880, 0), True, False), Borders(800, 1, (550, 631), False, True),
           Borders(1, 20, (1349, 630), True, True), Borders(1, 20, (550, 630), True, False),
           Borders(800, 1, (550, 650), False, False), Borders(400, 1, (750, 331), False, True),
           Borders(1, 20, (1149, 330), True, True), Borders(1, 20, (750, 330), True, False),
           Borders(400, 1, (750, 350), False, False), Borders(1900, 1, (0, 0), False, False)]
bullets = []

running = True
while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    screen.fill((43, 45, 47))
    for block in blocks:
        block.update(dt)
    for player in players:
        player.update(dt)
    for bullet in bullets:
        bullet.update(dt)
        if bullet.bounces > bullet.bounce_potential:
            bullets.remove(bullet)
    pygame.display.flip()
    if event.type == pygame.MOUSEBUTTONDOWN and players[0].bullets > len(bullets):
        x, y = pygame.mouse.get_pos()
        x -= players[0].pos[0]
        y -= players[0].pos[1]
        z = (x**2 + y**2)**(1/2)
        x /= z
        y /= z
        bullets.append(Bullet(0, x, y, 0, 0, 10, 10, 1000*x, 1000*y))


            
            
pygame.quit()