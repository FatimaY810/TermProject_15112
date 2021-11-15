import pygame
import random

score = 0
scrollY = 0

clock = pygame.time.Clock()

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font1 = pygame.font.match_font("calibri")

pygame.display.set_caption("(Not!) Crossy Road")

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

click = False

running = True

menuScreenImg = pygame.image.load("MenuScreen.png")

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font1, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def menuScreen():
    while True:
        screen.fill((65,156,3))
        screen.blit(menuScreenImg,(-10, 50))
        draw_text(screen, "Click grey button to start", 18, SCREEN_WIDTH//2, 400)
        draw_text(screen, "Press ESC to quit", 18, SCREEN_WIDTH//2, 420)
        draw_text(screen, "Press i for game instructions", 18, SCREEN_WIDTH//2, 440)
        
        
        startButton = pygame.Rect(SCREEN_WIDTH//2,400,100,50)
        startButton.midtop = (SCREEN_WIDTH//2,500)
        
        mx,my = pygame.mouse.get_pos()
    
        pygame.draw.rect(screen,(128,128,128), startButton)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(event.pos):
                    click = True
                    gameScreen()
                    
        pygame.display.update()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        global scrollY
        super(Player,self).__init__()
        self.playerIMG = [] #duck sprite facing up
        self.playerIMGRight = [] #duck sprite facing left
        self.walk1 = pygame.image.load("DuckWalk1.png").convert()
        self.walk1.set_colorkey((0, 0, 0), RLEACCEL) ##render each image to get rid of the black background
        self.playerIMG.append(self.walk1)
        self.walk2 = pygame.image.load("DuckWalk2.png").convert()
        self.walk2.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk1)
        self.walk3 = pygame.image.load("DuckRight.png").convert()
        self.walk3.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk3)
        self.walk4 = pygame.image.load("DuckRight2.png").convert()
        self.walk4.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk4)
        self.walk5 = pygame.image.load("DuckRight3.png").convert()
        self.walk5.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk5)
        self.walk6 = pygame.image.load("DuckRight4.png").convert()
        self.walk6.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk6)
        
        
        self.indexUp = 0
        self.indexRight = 0
        
        self.image = self.playerIMG[self.indexUp]
      
        self.rect = self.image.get_rect(topleft=(225,750))
        ##grabs rectangle attributes from rect class
        
    def update(self,pressed_keys):
        global scrollY
        ##moving the sprite
        if pressed_keys[K_UP]:
            scrollY -= 5
            self.indexRight = 0
            if self.indexUp == 0:
                self.image = self.playerIMG[0]
            if self.indexUp >=2:
                self.indexUp = 0
                self.image = self.playerIMG[self.indexUp]
            self.rect.move_ip(0,-5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.indexRight += 1
            self.indexUp = 0
            if self.indexRight == 0:
                self.image = self.playerIMGRight[0]
            if self.indexRight >= 4:
                self.indexRight = 0
                self.image = self.playerIMGRight[self.indexRight]
            self.rect.move_ip(5,0)
            
            
        ##keeping it on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 750
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

player1 = Player()
all_sprites = pygame.sprite.Group()
all_obstacles = pygame.sprite.Group()
all_sprites.add(player1)
score = 0

##OBSRACLES##

class cars(pygame.sprite.Sprite):
    
    def __init__(self):
        global scrollY
        super(cars,self).__init__()
        self.roadLane = pygame.Surface((600, 50))
        self.roadLane.fill((128,128,128))
        self.roadLaneRect = self.roadLane.get_rect(center=(SCREEN_WIDTH,100 + scrollY))
        self.listOfCars = ["brown","blue","yellow"]
        self.color = random.choice(self.listOfCars)
        if self.color == "brown":
            self.car1 = pygame.image.load("brownCar.png").convert()
        elif self.color == "blue":
            self.car1 = pygame.image.load("blueCar.png").convert()
        elif self.color == "yellow":
            self.car1 = pygame.image.load("yellowCar.png").convert()
        
    
        
def gameScreen():
    listOfObstacles = ["car","train","river"]
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()
                
        pressed_keys = pygame.key.get_pressed()
        player1.update(pressed_keys)
        
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
                
        screen.fill((65,156,3))
        
        all_sprites.draw(screen)
        
        pygame.display.flip()
        
        clock.tick(15) ##fps
        
        
        
menuScreen()
