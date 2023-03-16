
import pygame
import time
from random import randint as rand

pygame.init()
#setting variables
s_width, s_height = 1920, 1080
screen = pygame.display.set_mode([s_width,s_height])
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#s_width, s_height = pygame.display.get_surface().get_size()
print(s_width, s_height)
g = 9.8*4
ydrag = 0.8
xdrag = 0.5
drag = 0.6
#xvdrag = 0.1/0.13
xvdrag = 1
clock = pygame.time.Clock()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
k_t = pygame.image.load("kirby.png")
k = pygame.image.load("kirby_two_.png")
k_t_f = pygame.image.load("kirby_flip.png")
k_f = pygame.image.load("kirby_two_flip.png")
radius = 40


plus_mag = {"name" : "Bigger Mags",
            "power" : 5,
            "mag" : 1,
            "dmg" : 0,
            "hlth" : 0}
plus_dmg = {"name" : "Plus Damage",
            "power" : 8,
            "mag" : 0,
            "dmg" : 1,
            "hlth" : 0}
plus_hlth = {"name" : "Bigger Heart",
            "power" : 7,
            "mag" : 0,
            "dmg" : 0,
            "hlth" : 2}
plus_rad = {"name" : "Bigger Bullets",
            "power" : 4,
            "mag" : 0,
            "dmg" : 0.5,
            "hlth" : 0}
plus_plus_dmg = {"name" : "Super Damage",
            "power" : 10,
            "mag" : -1,
            "dmg" : 3,
            "hlth" : 0}
no_mag = {"name" : "Infinitely Big Mags",
            "power" : 8,
            "mag" : 10,
            "dmg" : -1,
            "hlth" : 0}
plus_size = {"name" : "Size Up",
            "power" : 5,
            "mag" : 0,
            "dmg" : 0,
            "hlth" : 1}
less_size = {"name" : "Size Down",
            "power" : 5,
            "mag" : 0,
            "dmg" : 0,
            "hlth" : -1}
plus_life = {"name" : "Extra Life",
            "power" : 10,
            "mag" : 0,
            "dmg" : 0,
            "hlth" : 5}

pwr_names = [plus_mag, plus_dmg, plus_hlth, plus_rad, plus_plus_dmg, no_mag, plus_size, less_size, plus_life]

def powerup_selection(shot, deaths, opp_deaths, opp_health, opp_shot, player_num):
    possible_powerups = pwr_names
    if deaths - opp_deaths >= 3:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["power"] < 7:
                possible_powerups.pop(i)
            else:
                i += 1
    if opp_health > 250:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["power"] < 7:
                possible_powerups.pop(i)
            else:
                i += 1
    if 10 < shot < 40:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["dmg"] < 0:
                possible_powerups.pop(i)
            else:
                i += 1
    if shot > 70:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["mag"] < 0:
                possible_powerups.pop(i)
            else:
                i += 1
    if opp_shot < 40:
        i = 0
        while i < len(possible_powerups):
            if pwr_names[i]["hlth"] < 0:
                possible_powerups.pop(i)
            else:
                i += 1
    a = rand(0,len(possible_powerups)-1)
    b = rand(0,len(possible_powerups)-1)
    c = rand(0,len(possible_powerups)-1)
    while b == a:
        b = rand(0,len(possible_powerups)-1)
    while c == a or b == c:
        c = rand(0, len(possible_powerups)-1)
    final_powerups = [possible_powerups[a], possible_powerups[b], possible_powerups[c]]
    print(f"Enter 1 for {final_powerups[0]}\n"
          f"Enter 2 for {final_powerups[1]}\n"
          f"Enter 3 for {final_powerups[2]}\n")
    picked = int(input("Which powerup would you like?"))
    players[player_num].powerups = final_powerups[picked-1]
    return possible_powerups









class Blocks:
    def __init__(self, width=10, height=10, pos=(1900,0), image = None):
        self.width = width
        self.height = height
        self.pos = pos
        self.image = pygame.transform.scale(image, (int(self.width), int(self.height)))
        
    def update(self, dt):
        self.draw()

    def draw(self):
        #drawing the surfaces in the game
        screen.blit(self.image,(self.pos[0], self.pos[1]))

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
    def __init__(self, radius=70, pos=(1900, 0), colour=(255, 255, 255), num = 1, keyup = None, keydown = None,
                 keyleft = None, keyright = None,pl = 0,bullets = 10, xvel=0, yvel=0, xacc=0, yacc=0, last_jump = 0, health = 500, deaths = 0, guid = 0, image = None, shot=0, powerup = None, dmg_mlt = 1, blt_size = 1):
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
        self.image = pygame.transform.scale(image,(int(self.radius * 2), int(self.radius *2)))
        self.shot = shot
        self.powerup = powerup
        self.dmg_mlt = dmg_mlt
        self.blt_size = blt_size




    def update(self, dt):
        self.ground = False
        self.yacc = self.yacc * ydrag
        self.yvel += (self.yacc + g)
        self.xacc = self.xacc * xdrag * dt
        self.xvel += self.xacc * dt
        self.xvel = self.xvel * xvdrag
        if self.health <= 0:
            powerup_selection(self.shot, self.deaths, players[-1 * (self.num - 1)].deaths, players[-1 * (self.num - 1)].health, players[-1 * (self.num - 1)].shot, self.num)
            self.health = 500
            players[-1 * (self.num - 1)].health = 500
            self.deaths += 1
            self.shot = 0
            players[-1 * (self.num - 1)].shot = 0
            self.pos = (s_width * 2 / 3, s_height / 1.3)
            players[-1 * (self.num - 1)].pos = (s_width / 3, s_height / 1.3)
            if self.powerup["name"] == "Bigger Bullets":
                self.blt_size += 1
            elif self.powerup["name"] == "Size Up":
                self.radius *= 1.5
                self.image = pygame.transform.scale(self.image, (int(self.radius * 2), int(self.radius * 2)))
            elif self.powerup["name"] == "Size Down":
                self.radius *= 0.5
                self.image = pygame.transform.scale(self.image, (int(self.radius * 2), int(self.radius * 2)))
            self.dmg_mlt += self.powerup["dmg"]
            self.health += self.powerup["hlth"] * 100
            self.bullets += self.powerup["mag"] * 20
            if self.bullets < 5:
                self.bullets = 5
            if self.dmg_mlt <= 0:
                self.dmg_mlt = 0.5
            if self.health <= 100:
                self.health = 100
            self.powerup = None





        self.pos = (self.pos[0]+(self.xvel * dt), self.pos[1]+(self.yvel * dt))
        if self.pos[1] > s_height-20:
            self.pos = (self.pos[0], s_height - self.radius - 40)
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
            self.shot = 0
            players[-1 * (self.num - 1)].shot = 0
            players[-1*(self.num-1)].deaths = 0
            players[-1*(self.num-1)].health = 500
            self.pos = (s_width*2/3, s_height/1.3)
            players[-1 * (self.num - 1)].pos = (s_width/3, s_height/1.3)
            self.powerups = []
            players[-1 * (self.num - 1)].powerups = []





        self.draw()
    
    def draw(self):
        #drawing the players in the game
        #pygame.draw.circle(screen, self.colour, (int(self.pos[0]), int(self.pos[1])-1), self.radius)
        screen.blit(self.image,(int(self.pos[0]-self.radius), int(self.pos[1]-self.radius+5)))

class Bullet:
    def __init__(self, pl, xdir, ydir, bounces = 0, bounce_potential = 0, dmg = 10, radius = 10, xvel = 10, yvel = 10):
        self.pl = pl
        self.xdir = xdir
        self.ydir = ydir
        self.pos = (players[pl].pos[0],players[pl].pos[1])
        self.bounces = bounces
        self.bounce_potential = bounce_potential
        self.dmg = dmg
        self.radius = radius * players[self.pl].blt_size
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
                player.health -= 10 * players[self.pl].dmg_mlt
        self.draw()

    def draw(self):
        pygame.draw.circle(screen, (255,255,255), (int(self.pos[0]), int(self.pos[1])), self.radius)


#creating players and surfaces
players = [Players(radius, (s_width*2/3, s_height/1.3), (2, 148, 165),num = 0,keyup = pygame.K_UP,keydown = pygame.K_DOWN,
                   keyleft = pygame.K_LEFT, keyright = pygame.K_RIGHT, pl = 0, bullets = 10, image = pygame.image.load("kirby_two_.png"))
    , Players(radius, (s_width/3, s_height/1.3), (193, 64, 61),num = 1,keyup = pygame.K_w,keydown = pygame.K_s,keyleft = pygame.K_a,
              keyright = pygame.K_d, pl = 1, bullets = 10, image = pygame.image.load("kirby.png"))]



blocks = []
borders = []

players[0].guid = joysticks[0].get_id()
players[1].guid = joysticks[1].get_id()


def block_and_border(width, height, x, y, image):
    blocks.append(Blocks(width, height, (x, y), image))
    borders.append(Borders(width, 1, (x, y), False, True))
    borders.append(Borders(width, 1, (x, y+height), False, False))
    borders.append(Borders(1, height, (x, y), True, False))
    borders.append(Borders(1, height, (x+width, y), True, True))



block_and_border(s_width, 40, 0, s_height-40, pygame.image.load("wall.png"))
block_and_border(40, s_height, 0, 0, pygame.image.load("wall.png"))
block_and_border(40, s_height, s_width-40, 0, pygame.image.load("wall.png"))
block_and_border(s_width, 40, 0, 0, pygame.image.load("wall.png"))
block_and_border(s_width*0.35, 40, s_width*0.25, s_height*0.62, pygame.image.load("platform.png"))
block_and_border(s_width*0.2, 40, s_width*0.65, s_height*0.3, pygame.image.load("platform.png"))
block_and_border(s_width*0.17, s_width*0.17, s_width*0.83, s_height-s_width*0.17, pygame.image.load("wall_2.png"))
block_and_border(40, s_height*0.25, s_width*0.27, s_height*0.15, pygame.image.load("wall.png"))
block_and_border(40, s_height*0.3, s_width*0.17, s_height-s_width*0.17, pygame.image.load("wall.png"))
block_and_border(s_height*0.3, 40, s_width*0.17-s_height*0.3, s_width*0.17, pygame.image.load("wall.png"))
block_and_border(s_height*0.3, 40, s_width*0.27, s_height*0.275-20, pygame.image.load("wall.png"))



bullets = []

running = True
while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            if event.instance_id == players[0].guid:
                pl_id = 0
            elif event.instance_id == players[1].guid:
                pl_id = 1
            if event.button == 0 and players[pl_id].ground:
                players[pl_id].yvel += -2000
                players[pl_id].ground = False
            if event.button == 12:
                players[pl_id].yacc += 600

        if event.type == pygame.JOYAXISMOTION:
            if event.instance_id == players[0].guid:
                pl_id = 0
            elif event.instance_id == players[1].guid:
                pl_id = 1
            if event.axis == 0:
                if event.value > 0.1 or event.value < -0.1:
                    players[pl_id].xvel = 1000*event.value
                    if event.value > 0 and pl_id == 0:
                        players[pl_id].image = pygame.transform.scale(k,(2*radius, 2*radius))
                    elif event.value < 0 and pl_id == 0:
                        players[pl_id].image = pygame.transform.scale(k_f,(2*radius, 2*radius))
                    elif event.value < 0 and pl_id == 1:
                        players[pl_id].image = pygame.transform.scale(k_t_f,(2*radius, 2*radius))
                    elif event.value > 0 and pl_id == 1:
                        players[pl_id].image = pygame.transform.scale(k_t,(2*radius, 2*radius))

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
            if event.instance_id == players[0].guid:
                pl_id = 0
            elif event.instance_id == players[1].guid:
                pl_id = 1
            x, y = joysticks[pl_id].get_axis(2), joysticks[pl_id].get_axis(3)
            bullets.append(Bullet(pl_id, x, y, 0, 0, 10, 10, 2000*x, 2000*y))
            players[pl_id].shot += 1
            print(players[pl_id].shot)



            
            
pygame.quit()
