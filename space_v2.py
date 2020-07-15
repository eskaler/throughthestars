import sys

import pygame
from pygame.locals import *

from math import sin, cos, atan, tan, sqrt
from random import randint

class star:

    x = y = hyp = size = alpha = step = index = 0.0
    scf = 30 #size change frequency
    prevx = prevy = 0
    color = (0,0,0)
    def __init__(self, i):
        self.x = self.y = 0
        while self.x==0 or self.y==0:
            self.x = randint(-RD, RD)
            self.y = randint(-RD, RD)
        if(abs(self.x) in range(int(RD/2), RD)) or (abs(self.y) in range(int(RD/2),RD)):
            self.scf = 30
        if(abs(self.x) in range(int(RD/3), int(RD/2))) or (abs(self.y) in range(int(RD/3),int(RD/2))):
            self.scf = 25
        if(abs(self.x) in range(int(RD/4), int(RD/3))) or (abs(self.y) in range(int(RD/4),int(RD/3))):
            self.scf = 20
        self.alpha = atan(float(self.y)/float(self.x))
        self.hyp = sqrt(self.x**2 + self.y**2)
        self.step = 1#randint(5, 10)
        self.size = 1
        #print "spawned (x,y,alpha,hyp):", self.x, self.y, self.alpha, self.hyp, "\n"
        self.prevx = self.x
        self.prevy = self.y
        self.index = i
        self.color = COLORS[self.size]

    def xyMove(self, i):
        self.prevx = self.x
        self.prevy = self.y
        checkX = False if self.x>0 else True
        self.x = cos(self.alpha)*self.hyp
        if self.x>0 and checkX:
            self.x = -self.x
        if self.x<0 and not checkX:
            self.x = -self.x
        checkY = False if self.y>0 else True
        #print "y, alpha:",self.y, self.alpha
        self.y = sin(self.alpha)*self.hyp
       # print "y:",self.y,"\n"
        if self.y>0 and checkY:
            self.y = -self.y
        if self.y<0 and not checkY:
            self.y = -self.y
        if i%self.scf==0:
            #self.scf/10
            self.color = COLORS[self.size]
        if i%(self.scf*2)==0:
            self.size+=1
        self.hyp+=self.step
        self.step+=0.05

    def checkOut(self, h, w):
        if (int(w/2)-abs(self.x)<0) or (int(w/2)+abs(self.x)>w) or (int(h/2)-abs(self.y)<0) or (int(h/2)+abs(self.y)>h):
            return True
        else:
            return False

pygame.init()
pygame.font.init()

W = 1366
H = 768
SF = 1    #star frequency | bigger value - less stars
RD = 300   #random distance
FPS = 60
WHITE=(255,255,255)
BLACK=(0,0,0)
COLORS = [BLACK, (48,48,48), (88,88,88), (169,169,169), (220,220,220),  WHITE, WHITE, WHITE, WHITE, WHITE]


DISPLAY = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption('SPACE')
DISPLAY.fill(BLACK)
fpsClock = pygame.time.Clock()


#ship = pygame.image.load('ship1.png')
i = 0
stars = []
while True:
    DISPLAY.fill(BLACK)
    if i%SF==0:
        stars.append(star(i))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            stars.append(star(i))
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
            FPS += 5
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
            if FPS>10:
                FPS -= 5
    for item in stars:
        if item.checkOut(H,W):
            stars = [z for z in stars if z.index != item.index]
        pygame.draw.circle(DISPLAY, item.color, (int(item.x+W/2), int(item.y+H/2)), int(item.size))
        item.xyMove(i)
        #pygame.draw.line(DISPLAY, item.color, (int(item.prevx)+W/2, int(item.prevy)+H/2), (int(item.x)+W/2, int(item.y)+H/2), 4)
        #print item.x, item.y, item.hyp, item.size

    #pygame.draw.circle(DISPLAY, (255,0,0), (W/2, H/2), 1)
    #pygame.draw.line(DISPLAY, (255,0,0), (0, H/2),(W, H/2))  #draw middle of the screen
    #pygame.draw.line(DISPLAY, (255,0,0), (W/2, 0),(W/2, H))
    i += 1
    #DISPLAY.blit(ship, (0,0))
    print (len(stars))
    pygame.display.update()
    fpsClock.tick(FPS)
