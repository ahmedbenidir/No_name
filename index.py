import pygame as pg
import random
pg.init()

win = pg.display.set_mode((800,480))
pg.display.set_caption('First game')

walkRight = [pg.image.load('img/hero/R1.png'), pg.image.load('img/hero/R2.png'), pg.image.load('img/hero/R3.png'), pg.image.load('img/hero/R4.png'), pg.image.load('img/hero/R5.png'), pg.image.load('img/hero/R6.png'), pg.image.load('img/hero/R7.png'), pg.image.load('img/hero/R8.png'), pg.image.load('img/hero/R9.png')]
walkLeft = [pg.image.load('img/hero/L1.png'), pg.image.load('img/hero/L2.png'), pg.image.load('img/hero/L3.png'), pg.image.load('img/hero/L4.png'), pg.image.load('img/hero/L5.png'), pg.image.load('img/hero/L6.png'), pg.image.load('img/hero/L7.png'), pg.image.load('img/hero/L8.png'), pg.image.load('img/hero/L9.png')]
bg = pg.image.load('img/bg.jpg')
char = pg.image.load('img/hero/standing.png')

clock = pg.time.Clock()
score = 0

bulletSound = pg.mixer.Sound('sound/bullet.wav')
hitSound = pg.mixer.Sound('sound/death.wav')
music = pg.mixer.music.load('sound/music.mp3')

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # NEW
        #pg.draw.rect(win, (255,0,0), self.hitbox,2) # To draw the hit box around the player

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60 # We are resetting the player position
        self.y = 410
        self.walkCount = 0
        font1 = pg.font.SysFont('comicsans', 100)
        text = font1.render('Game over', 1, (255,0,0))
        win.blit(text, (400 - (text.get_width()/2),200))
        pg.display.update()
        i = 0
        while i < 300:
            pg.time.delay(10)
            i += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    i = 301
                    pg.quit()

        # After we are hit we are going to display a message to the screen for
        # a certain period of time

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pg.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pg.image.load('img/enemy/R1E.png'), pg.image.load('img/enemy/R2E.png'), pg.image.load('img/enemy/R3E.png'), pg.image.load('img/enemy/R4E.png'), pg.image.load('img/enemy/R5E.png'), pg.image.load('img/enemy/R6E.png'), pg.image.load('img/enemy/R7E.png'), pg.image.load('img/enemy/R8E.png'), pg.image.load('img/enemy/R9E.png'), pg.image.load('img/enemy/R10E.png'), pg.image.load('img/enemy/R11E.png')]
    walkLeft = [pg.image.load('img/enemy/L1E.png'), pg.image.load('img/enemy/L2E.png'), pg.image.load('img/enemy/L3E.png'), pg.image.load('img/enemy/L4E.png'), pg.image.load('img/enemy/L5E.png'), pg.image.load('img/enemy/L6E.png'), pg.image.load('img/enemy/L7E.png'), pg.image.load('img/enemy/L8E.png'), pg.image.load('img/enemy/L9E.png'), pg.image.load('img/enemy/L10E.png'), pg.image.load('img/enemy/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 1
        self.visible = True
        self.live = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33: # Since we have 11 images for each animtion our upper bound is 33.
                                         # We will show each image for 3 frames. 3 x 11 = 33.
                self.walkCount = 0

            if self.vel > 0: # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:  # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57) # NEW
            #pg.draw.rect(win, (255,0,0), self.hitbox,2) # Draws the hit box around the enemy
            pg.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # NEW
            pg.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (50 * (1 - self.health)), 10)) # NEW


    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else: # If we are moving left
            if self.x > self.path[0] - self.vel: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health >0:
            self.health-=1
        else:
            self.visible = False
            self.live = False


def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score : '+str(score), 1, (0,0,0))
    win.blit(text,(700,10))
    man.draw(win)
    goblin.draw(win)
    goblin2.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pg.display.update()


#mainloop
font = pg.font.SysFont('comicsans', 20, True)
man = player(400, 404, 64,64)
goblin = enemy(random.randrange(0, 499), 410, 64, 64, random.randrange(500, 720))
goblin2 = enemy(720, 410, 64, 64, 50)
bullets = []
shootLoop = 0
run = True
while run:
    clock.tick(27)

    if goblin.visible == False:
        goblin = enemy(random.randrange(0, 720), 410, 64, 64, random.randrange(0, 720))
    if goblin2.visible == False:
        goblin2 = enemy(random.randrange(0, 720), 410, 64, 64, random.randrange(0, 720))

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                if score <= 0:
                    score = 0
                else:
                    score -= 1
            # This will go at the top of or main loop.
    if goblin2.visible == True:
        if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                man.hit()
                if score <= 0:
                    score = 0
                else:
                    score -= 1

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: # Checks x coords
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: # Checks y coords
                    goblin.hit() # calls enemy hit method
                    score += 1
                    hitSound.play()
                    bullets.pop(bullets.index(bullet)) # removes bullet from bullet list

        if goblin2.visible == True:
            if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]: # Checks x coords
                if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]: # Checks y coords
                    goblin2.hit() # calls enemy hit method
                    score += 1
                    hitSound.play()
                    bullets.pop(bullets.index(bullet)) # removes bullet from bullet list

        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pg.key.get_pressed()

    if keys[pg.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

        shootLoop = 1
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pg.K_RIGHT] and man.x < 800 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pg.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pg.quit()
