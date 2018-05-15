import pygame
import tiles

#make constants and colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,180,0)
SKYCOLOR = (142, 185, 255)
WIDTH = 960
HEIGHT = 640

#start the pygame engine
pygame.init()

#make images
pHead = pygame.image.load("/Users/jeffreyleemacbookpro/Desktop/Platformer Art Complete Pack/Base pack/HUD/hud_p1.png")

eHead = pygame.image.load("/Users/jeffreyleemacbookpro/Desktop/Platformer Art Complete Pack/Extra animations and enemies/Alien sprites/alienBlue_badge2.png")

dirt = pygame.image.load("/Users/jeffreyleemacbookpro/Desktop/Platformer Art Complete Pack/Base pack/Tiles/grassCenter.png")
grass = pygame.image.load("/Users/jeffreyleemacbookpro/Desktop/Platformer Art Complete Pack/Base pack/Tiles/grassMid.png")
metal = pygame.image.load("/Users/jeffreyleemacbookpro/Desktop/Platformer Art Complete Pack/Request pack/Tiles/metalCenter.png")
cloud = pygame.image.load("/Users/jeffreyleemacbookpro/Desktop/Platformer Art Complete Pack/Base pack/Items/cloud3.png")

#create a display screen and clock
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

#give window a name
pygame.display.set_caption("PathFinder")

#generate the grid
gridList = [[0]*30 for n in range(20)]

class Grid:
    def draw(self):
        #draw the grid
        x, y = 0, 0
        for row in gridList:
            for col in row:
                if col == 1:
                    screen.blit(pHead,[x, y])
                if col == 2:
                    screen.blit(eHead,[x,y])
                if col == "dirt":
                    screen.blit(dirt,[x,y])
                if col == "grass":
                    screen.blit(grass,[x,y])
                if col == "metal":
                    screen.blit(metal,[x,y])
                if col == "cloudS":
                    screen.blit(cloud,[x,y])
                x += 32
            y += 32
            x = 0

grid = Grid()

#make the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        gridList[self.y][self.x] = 1

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            gridList[self.y][self.x] = 0
            self.y -= 1
            if self.y < 0:
                self.y += 1
            elif gridList[self.y][self.x] != 1 and gridList[self.y][self.x] != 0:
                self.y += 1

        if keys[pygame.K_a]:
            gridList[self.y][self.x] = 0
            self.x -= 1
            if self.x < 0:
                self.x += 1
            elif gridList[self.y][self.x] != 1 and gridList[self.y][self.x] != 0:
                self.x += 1

        if keys[pygame.K_s]:
            gridList[self.y][self.x] = 0
            self.y += 1
            if self.y >= 20:
                self.y -= 1
            elif gridList[self.y][self.x] != 1 and gridList[self.y][self.x] != 0:
                self.y -= 1

        if keys[pygame.K_d]:
            gridList[self.y][self.x] = 0
            self.x += 1
            if self.x >= 30:
                self.x -= 1
            elif gridList[self.y][self.x] != 1 and gridList[self.y][self.x] != 0:
                self.x -= 1

    def update(self):
        self.move()
        gridList[self.y][self.x] = 1

#make the enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        gridList[self.y][self.x] = 2

    def update(self):
        gridList[self.y][self.x] = 2

class SingleTile(pygame.sprite.Sprite):
    def __init__(self,image,type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        gridList[self.y][self.x] = self.type

    def update(self):
        gridList[self.y][self.x] = self.type

class MultiTile(pygame.sprite.Sprite):
    def __init__(self,image,source,type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.source = source
        gridList[self.y][self.x] = self.source
        if self.type == "cloud":
            gridList[self.y][self.x+1] = self.type


    def update(self):
        if self.type == "cloud":
            gridList[self.y][self.x] = self.source
            gridList[self.y][self.x+1] = self.type

#make the sprite groups

all_sprites = pygame.sprite.Group()
player = Player(pHead,15,9)
all_sprites.add(player)

enemies = pygame.sprite.Group()
enemy = Enemy(eHead,2,12)
enemies.add(enemy)

tiles = pygame.sprite.Group()

#make the base dirt and grass
for x in range(30):
    for y in range(18,20):
        tiles.add(SingleTile(dirt,"dirt",x,y))

for x in range(16,30):
    for y in range(11,18):
        tiles.add(SingleTile(dirt, "dirt", x, y))

for x in range(16):
    tiles.add(SingleTile(grass,"grass",x,17))

for x in range(16,30):
    tiles.add(SingleTile(grass,"grass",x,10))

#make the platforms
for y in range(1,6,2):
    tiles.add(MultiTile(cloud,"cloudS","cloud",y,14))

#make the platforms
for y in range(8,14,2):
    tiles.add(MultiTile(cloud,"cloudS","cloud",y,12))

#make the main game loop

running = True

while running == True:
    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update everything
    screen.fill(SKYCOLOR)
    tiles.update()
    all_sprites.update()
    enemies.update()
    grid.draw()

    #blit everything to screen
    pygame.display.flip()