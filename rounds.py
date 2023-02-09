
import pygame
import time
from random import randint as rand

pygame.init()
#setting variables
#s_width, s_height = 1900, 950
#screen = pygame.display.set_mode([s_width,s_height])
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
s_width, s_height = pygame.display.get_surface().get_size()
g = 9.8
ydrag = 0.8
xdrag = 0.5
drag = 0.6
#xvdrag = 0.1/0.13
xvdrag = 1
clock = pygame.time.Clock()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

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
        pygame.draw.rect(screen, self.colour, pygame.Rect(int(self.pos[0]), int(self.pos[1]), int(self.width), int(self.height)))

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
                 keyleft = None, keyright = None,pl = 0,bullets = 10, xvel=0, yvel=0, xacc=0, yacc=0, last_jump = 0, health = 500, deaths = 0, guid = 0, image = None):
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
        self.deaths = deaths
        self.guid = guid
        self.image = image
        self.image = pygame.transform.scale(image,(int(image.get_width()* 0.2), int(image.get_height()*0.2)))


    def update(self, dt):
        self.ground = False
        self.yacc = self.yacc * ydrag
        self.yvel += (self.yacc + g)
        self.xacc = self.xacc * xdrag * dt
        self.xvel += self.xacc * dt
        self.xvel = self.xvel * xvdrag
        if self.health <= 0:
            self.pos = (s_width/2,s_height/2)
            self.health = 500
            self.deaths += 1




        self.pos = (self.pos[0]+(self.xvel * dt), self.pos[1]+(self.yvel * dt))
        #Collision detection between players and surfaces
        for border in borders:
            if border.pos[1] == s_height-20 and -1 < (self.pos[1] + self.radius) - border.pos[1]:
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

        if self.deaths == 5:
            for t in range(1000):
                screen.fill((138, 40, 33))
                pygame.display.flip()
            self.deaths = 0
            players[-1*(self.num-1)].deaths = 0
            players[-1*(self.num-1)].health = 500
            self.pos = (s_width*2/3, s_height/1.3)
            players[-1 * (self.num - 1)].pos = (s_width/3, s_height/1.3)





        self.draw()
    
    def draw(self):
        #drawing the players in the game
        #pygame.draw.circle(screen, self.colour, (int(self.pos[0]), int(self.pos[1])-1), self.radius)
        screen.blit(self.image,(int(self.pos[0]), int(self.pos[1]-1)-self.image.get_height()/2))

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
        self.yvel += g
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
players = [Players(30, (s_width*2/3, s_height/1.3), (2, 148, 165),num = 0,keyup = pygame.K_UP,keydown = pygame.K_DOWN,
                   keyleft = pygame.K_LEFT, keyright = pygame.K_RIGHT, pl = 0, bullets = 10, image = pygame.image.load("Kirby.png").convert_alpha())
    , Players(30, (s_width/3, s_height/1.3), (193, 64, 61),num = 1,keyup = pygame.K_w,keydown = pygame.K_s,keyleft = pygame.K_a,
              keyright = pygame.K_d, pl = 1, bullets = 10, image = pygame.image.load("Kirby.png").convert_alpha())]



blocks = []
borders = []

#players[0].guid = joysticks[0].get_guid()
#players[1].guid = joysticks[1].get_guid()
def block_and_border(width, height, x, y):
    blocks.append(Blocks(width, height, (x, y), (255, 255, 255)))
    borders.append(Borders(width, 1, (x, y), False, True))
    borders.append(Borders(width, 1, (x, y+height), False, False))
    borders.append(Borders(1, height, (x, y), True, False))
    borders.append(Borders(1, height, (x+width, y), True, True))



block_and_border(s_width, 20, 0, s_height-20)
block_and_border(20, s_height, 0, 0)
block_and_border(20, s_height, s_width-20, 0)
block_and_border(s_width, 20, 0, 0)
block_and_border(s_width*0.5, 20, s_width*0.25, s_height*0.62)
block_and_border(s_width*0.25, 20, s_width*0.375, s_height*0.3)


bullets = []

running = True
while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            if event.guid == players[0].guid:
                pl_id = 0
            elif event.guid == players[1].guid:
                pl_id = 1
            if event.button == 0 and players[pl_id].ground:
                players[pl_id].yvel += -3000
                players[pl_id].ground = False
            if event.button == 12:
                players[pl_id].yacc += 10000

        if event.type == pygame.JOYAXISMOTION:
            if event.guid == players[0].guid:
                pl_id = 0
            elif event.guid == players[1].guid:
                pl_id = 1
            if event.axis == 0:
                if event.value > 0.1 or event.value < -0.1:
                    players[pl_id].xvel = 1000*event.value
                else:
                    players[pl_id].xvel = 0


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
    for player in players:
        if event.type == pygame.JOYAXISMOTION and event.axis == 5 and player.bullets > len(bullets):
            if event.guid == players[0].guid:
                pl_id = 0
            elif event.guid == players[1].guid:
                pl_id = 1
            x, y = joysticks[pl_id].get_axis(2), joysticks[pl_id].get_axis(3)
            bullets.append(Bullet(pl_id, x, y, 0, 0, 10, 10, 2000*x, 2000*y))


            
            
pygame.quit()
