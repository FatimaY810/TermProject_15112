import pygame
import random

score = 0
##the score
scrollY = 0
##how much the background should scroll
carsOnScreen = 0
##to keep only one car on the screen at once
##no overlapping of cars
roadOnScreen = False
riverOnScreen = False
counter = 0
duck = False
dog = False
player1 = None
player2 = None
carOnRoadList = []
index = 0
multiplayer = False
singlePlayer = False
mouseClicks = 0
powerUpCounter = 0
poweredUp = False
poweredUp1 = False
poweredUp2 = False
powerUpCounter1 = 0
powerUpCounter2 = 0


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
    K_BACKSPACE,
    KEYDOWN,
    QUIT,
)

click = False

running = True

menuScreenImg = pygame.image.load("MenuScreen.png")
characterSelectImg = pygame.image.load("characterSelection.png")
multiplayerScreenImg = pygame.image.load("multiplayerScreen.png")
InstructionScreenImg = pygame.image.load("InstructionScreen.png")
GameOverScreenImg = pygame.image.load("gameOverScreen.png")
player1WinImg = pygame.image.load("player1Win.png")
player2WinImg = pygame.image.load("player2Win.png")


def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font1, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)
    
### class cloud code cited from realpython.com ###
    
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
     center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-2, 0)
        if self.rect.right < 0:
            self.kill()

####################################################

ADDCLOUD = pygame.USEREVENT + 4
pygame.time.set_timer(ADDCLOUD, 5000)

def menuScreen():
    pygame.sprite.Group.empty(all_obstacles)
    pygame.sprite.Group.empty(all_sprites)
    pygame.sprite.Group.empty(all_enemies)
    pygame.sprite.Group.empty(all_bridges)
    global die
    global carsOnScreen
    global roadOnScreen
    global scrollY
    global numberOfSteps
    global obstaclesOnScreen
    global riverOnScreen
    global score
    global counter
    global mouseClicks
    mouseClicks = 0
    die = False
    score = 0
    text = ""
    font = pygame.font.Font(None, 30)
    carsOnScreen = False
    roadOnScreen = False
    scrollY = 0
    numberOfSteps = 0
    obstaclesOnScreen = False
    riverOnScreen = False
    counter = 0
    while True:
        screen.fill((65,156,3))
        screen.blit(menuScreenImg,(-10, 50))
        draw_text(screen, "Type START to go to character selection", 18, SCREEN_WIDTH//2, 400)
        draw_text(screen, "Press ESC to quit", 18, SCREEN_WIDTH//2, 420)
        draw_text(screen, "Type i for game instructions", 18, SCREEN_WIDTH//2, 440)
        
        input_rect = pygame.Rect(SCREEN_WIDTH//2,550,150,50)
        input_rect.midtop = (SCREEN_WIDTH//2,600)
        color_active = pygame.Color("grey")
        color_inactive = pygame.Color("black")
        color = color_inactive
        
        active = False
        
        done = False
        
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[pygame.K_i]:
            instructionsScreen()
        
        while not done:
            mx,my = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if active == True:
                    color = color_active
                else:
                    color = color_inactive
                    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_RETURN:
                        if text == "START" or text == "start":
                            multiplayerChoice()
                        if text == "i" or text == "I":
                            instructionsScreen()
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                        
            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (input_rect.x+5,input_rect.y+5))
            pygame.draw.rect(screen,color, input_rect,2)
            
                        
            pygame.display.update()
            
def instructionsScreen():
    while True:
        screen.fill((65,156,3))
        screen.blit(InstructionScreenImg,(0, 50))
        
        returnButton = pygame.Rect((SCREEN_WIDTH//2)-50,550,100,50)
        
        for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if returnButton.collidepoint(event.pos):
                        menuScreen()
        
        pygame.draw.rect(screen,(100,100,100),returnButton)
        draw_text(screen, "Return", 20, SCREEN_WIDTH//2, 565)
    
    
        pygame.display.update()
        
        
            
def multiplayerChoice():
    global multiplayer
    global singlePlayer
    while True:
        mousePos = pygame.mouse.get_pos()
        
        screen.fill((65,156,3))
        screen.blit(multiplayerScreenImg,(-10, 50))
        
        button1 = pygame.Rect((SCREEN_WIDTH//3)-50,385,100,50)
        button2 = pygame.Rect((2*SCREEN_WIDTH//3)-50,385,100,50)
    
        
        for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1.collidepoint(event.pos):
                        singlePlayer = True
                        multiplayer = False
                        characterSelection()
                    elif button2.collidepoint(event.pos):
                        singlePlayer = False
                        multiplayer = True
                        characterSelection2()
         
        pygame.draw.rect(screen,(100,100,100),button1)
        pygame.draw.rect(screen,(100,100,100),button2)
        draw_text(screen, "1", 20, SCREEN_WIDTH//3, 400)
        draw_text(screen, "2", 20, 2*SCREEN_WIDTH//3, 400)        
        pygame.display.update()
        
            
        
def gameOverScreen():
    global score
    while True:
        screen.fill((65,156,3))
        screen.blit(GameOverScreenImg,(30, 50))
        
        returnButton = pygame.Rect((SCREEN_WIDTH//2)-50,550,100,50)
        
        for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if returnButton.collidepoint(event.pos):
                        menuScreen()
        
        pygame.draw.rect(screen,(100,100,100),returnButton)
        draw_text(screen, "Return", 20, SCREEN_WIDTH//2, 565)
        draw_text(screen, f" Final Score: {score//2}", 24, SCREEN_WIDTH/2, 500)
        pygame.display.update()
        
def gameOverScreenPlayer1():
    while True:
        screen.fill((65,156,3))
        screen.blit(player2WinImg,(10, 50))
        
        returnButton = pygame.Rect((SCREEN_WIDTH//2)-50,550,100,50)
        
        for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if returnButton.collidepoint(event.pos):
                        menuScreen()
        
        pygame.draw.rect(screen,(100,100,100),returnButton)
        draw_text(screen, "Return", 20, SCREEN_WIDTH//2, 565)
        pygame.display.update()
        
def gameOverScreenPlayer2():
    while True:
        screen.fill((65,156,3))
        screen.blit(player1WinImg,(10, 50))
        
        returnButton = pygame.Rect((SCREEN_WIDTH//2)-50,550,100,50)
        
        for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if returnButton.collidepoint(event.pos):
                        menuScreen()
        
        pygame.draw.rect(screen,(100,100,100),returnButton)
        draw_text(screen, "Return", 20, SCREEN_WIDTH//2, 565)
        pygame.display.update()
        

class Duck(pygame.sprite.Sprite):
    
    def __init__(self):
        global scrollY
        super(Duck,self).__init__()
        self.playerIMG = []
        #duck sprite facing up
        self.playerIMGRight = []
        #duck sprite facing right
        self.playerIMGLeft = []
        self.walk1 = pygame.image.load("DuckWalk1.png").convert()
        self.walk1.set_colorkey((0, 0, 0), RLEACCEL)
        ##render each image to get rid of the black background
        self.playerIMG.append(self.walk1)
        self.walk2 = pygame.image.load("DuckWalk2.png").convert()
        self.walk2.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk2)
        self.walk11 = pygame.image.load("DuckWalk3.png").convert()
        self.walk11.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk11)
        self.walk12 = pygame.image.load("DuckWalk4.png").convert()
        self.walk12.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk12)
        self.walk13 = pygame.image.load("DuckWalk5.png").convert()
        self.walk13.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk13)
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
        self.walk7 = pygame.image.load("Left1.png").convert()
        self.walk7.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk7)
        self.walk8 = pygame.image.load("Left2.png").convert()
        self.walk8.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk8)
        self.walk9 = pygame.image.load("Left3.png").convert()
        self.walk9.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk9)
        self.walk10 = pygame.image.load("Left4.png").convert()
        self.walk10.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk10)
        
        self.indexUp = 0
        self.indexRight = 0
        self.indexLeft = 0
        
        self.image = self.playerIMG[self.indexUp]
        
        if singlePlayer == True:
            self.rect = self.image.get_rect(topleft=(225,750))
            
        elif multiplayer == True:
            self.rect = self.image.get_rect(topleft=(150,750))
        ##grabs rectangle attributes from rect class
        
    def update(self,pressed_keys):
        global scrollY
        global score
        global player1
        global player2
        ##moving the sprite
        if isinstance(player1,Duck):
            if pressed_keys[K_UP]:
                score += 1
                scrollY += 15
                self.indexRight = 0
                self.indexLeft = 0
                self.indexUp += 1
                i = self.indexUp-1
                self.image = self.playerIMG[i]
                if self.indexUp >=4:
                    self.indexUp = 0
                    self.image = self.playerIMG[self.indexUp]
            if pressed_keys[K_LEFT]:
                self.indexLeft += 1
                self.indexRight = 0
                self.indexUp = 0
                i = self.indexLeft-1
                self.image = self.playerIMGLeft[i]
                if self.indexLeft >= 4:
                    self.indexLeft = 0
                    self.image = self.playerIMGLeft[self.indexLeft]
                self.rect.move_ip(-5,0)
            if pressed_keys[K_RIGHT]:
                self.indexRight += 1
                self.indexUp = 0
                self.indexLeft = 0
                i = self.indexRight-1
                self.image = self.playerIMGRight[i]
                if self.indexRight >= 4:
                    self.indexRight = 0
                    self.image = self.playerIMGRight[self.indexRight]
                self.rect.move_ip(5,0)
        elif isinstance(player2, Duck):
            if pressed_keys[pygame.K_w]:
                score += 1
                scrollY += 15
                self.indexRight = 0
                self.indexLeft = 0
                self.indexUp += 1
                i = self.indexUp-1
                self.image = self.playerIMG[i]
                if self.indexUp >=4:
                    self.indexUp = 0
                    self.image = self.playerIMG[self.indexUp]
            if pressed_keys[pygame.K_a]:
                self.indexLeft += 1
                self.indexRight = 0
                self.indexUp = 0
                i = self.indexLeft-1
                self.image = self.playerIMGLeft[i]
                if self.indexLeft >= 4:
                    self.indexLeft = 0
                    self.image = self.playerIMGLeft[self.indexLeft]
                self.rect.move_ip(-5,0)
            if pressed_keys[pygame.K_d]:
                self.indexRight += 1
                self.indexUp = 0
                self.indexLeft = 0
                i = self.indexRight-1
                self.image = self.playerIMGRight[i]
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

class Dog(pygame.sprite.Sprite):
    
    def __init__(self):
        global scrollY
        super(Dog,self).__init__()
        self.playerIMG = []
        #duck sprite facing up
        self.playerIMGRight = []
        #duck sprite facing right
        self.playerIMGLeft = []
        self.walk1 = pygame.image.load("dogFront1.png").convert()
        self.walk1.set_colorkey((0, 0, 0), RLEACCEL)
        ##render each image to get rid of the black background
        self.playerIMG.append(self.walk1)
        self.walk2 = pygame.image.load("dogFront2.png").convert()
        self.walk2.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk2)
        self.walk11 = pygame.image.load("dogFront3.png").convert()
        self.walk11.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk11)
        self.walk12 = pygame.image.load("dogFront4.png").convert()
        self.walk12.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMG.append(self.walk12)
        self.walk3 = pygame.image.load("dogRight1.png").convert()
        self.walk3.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk3)
        self.walk4 = pygame.image.load("dogRight2.png").convert()
        self.walk4.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk4)
        self.walk5 = pygame.image.load("dogRight3.png").convert()
        self.walk5.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk5)
        self.walk6 = pygame.image.load("dogRight4.png").convert()
        self.walk6.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGRight.append(self.walk6)
        self.walk7 = pygame.image.load("dogLeft1.png").convert()
        self.walk7.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk7)
        self.walk8 = pygame.image.load("dogLeft2.png").convert()
        self.walk8.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk8)
        self.walk9 = pygame.image.load("dogLeft3.png").convert()
        self.walk9.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk9)
        self.walk10 = pygame.image.load("dogLeft4.png").convert()
        self.walk10.set_colorkey((0, 0, 0), RLEACCEL)
        self.playerIMGLeft.append(self.walk10)
        
        self.indexUp = 0
        self.indexRight = 0
        self.indexLeft = 0
        
        self.image = self.playerIMG[self.indexUp]
      
        if singlePlayer == True:
            self.rect = self.image.get_rect(topleft=(225,750))
        
        elif multiplayer == True:
            self.rect = self.image.get_rect(topleft=(300,750))
        ##grabs rectangle attributes from rect class
        
    def update(self,pressed_keys):
        global player1
        global player2
        global scrollY
        global score
        ##moving the sprite
        if isinstance(player1,Dog):
            if pressed_keys[K_UP]:
                score += 1
                scrollY += 15
                self.indexRight = 0
                self.indexLeft = 0
                self.indexUp += 1
                i = self.indexUp-1
                self.image = self.playerIMG[i]
                if self.indexUp >=4:
                    self.indexUp = 0
                    self.image = self.playerIMG[self.indexUp]
            if pressed_keys[K_LEFT]:
                self.indexLeft += 1
                self.indexRight = 0
                self.indexUp = 0
                i = self.indexLeft-1
                self.image = self.playerIMGLeft[i]
                if self.indexLeft >= 4:
                    self.indexLeft = 0
                    self.image = self.playerIMGLeft[self.indexLeft]
                self.rect.move_ip(-5,0)
            if pressed_keys[K_RIGHT]:
                self.indexRight += 1
                self.indexUp = 0
                self.indexLeft = 0
                i = self.indexRight-1
                self.image = self.playerIMGRight[i]
                if self.indexRight >= 4:
                    self.indexRight = 0
                    self.image = self.playerIMGRight[self.indexRight]
                self.rect.move_ip(5,0)
        elif isinstance(player2, Dog):
            if pressed_keys[pygame.K_w]:
                score += 1
                scrollY += 15
                self.indexRight = 0
                self.indexLeft = 0
                self.indexUp += 1
                i = self.indexUp-1
                self.image = self.playerIMG[i]
                if self.indexUp >=4:
                    self.indexUp = 0
                    self.image = self.playerIMG[self.indexUp]
            if pressed_keys[pygame.K_a]:
                self.indexLeft += 1
                self.indexRight = 0
                self.indexUp = 0
                i = self.indexLeft-1
                self.image = self.playerIMGLeft[i]
                if self.indexLeft >= 4:
                    self.indexLeft = 0
                    self.image = self.playerIMGLeft[self.indexLeft]
                self.rect.move_ip(-5,0)
            if pressed_keys[pygame.K_d]:
                self.indexRight += 1
                self.indexUp = 0
                self.indexLeft = 0
                i = self.indexRight-1
                self.image = self.playerIMGRight[i]
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

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        self.IMGList = []
        super(Enemy,self).__init__()
        self.walk1 = pygame.image.load("monsterSprite.png").convert()
        self.walk1.set_colorkey((0, 0, 0), RLEACCEL)
        self.walk2 = pygame.image.load("monsterSprite2.png").convert()
        self.walk2.set_colorkey((0, 0, 0), RLEACCEL)
        self.walk3 = pygame.image.load("monsterSprite3.png").convert()
        self.walk3.set_colorkey((0, 0, 0), RLEACCEL)
        self.walk4 = pygame.image.load("monsterSprite4.png").convert()
        self.walk4.set_colorkey((0, 0, 0), RLEACCEL)
        self.walk5 = pygame.image.load("monsterSprite5.png").convert()
        self.walk5.set_colorkey((0, 0, 0), RLEACCEL)
        self.walk6 = pygame.image.load("monsterSprite6.png").convert()
        self.walk6.set_colorkey((0, 0, 0), RLEACCEL)
        self.walk7 = pygame.image.load("monsterSprite7.png").convert()
        self.walk7.set_colorkey((0, 0, 0), RLEACCEL)
        self.IMGList.append(self.walk1)
        self.IMGList.append(self.walk2)
        self.IMGList.append(self.walk3)
        self.IMGList.append(self.walk4)
        self.IMGList.append(self.walk5)
        self.IMGList.append(self.walk6)
        self.IMGList.append(self.walk6)
        self.i = 0
        self.image = self.IMGList[self.i%7]
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0-scrollY, 700-scrollY),
                )
            )
        self.speed = random.randint(5,20)
    
    def update(self,pressed_keys):
        self.i += 1
        self.image = self.IMGList[self.i%7]
        currentY = self.rect.y
        currentX = self.rect.x
        if pressed_keys[K_UP]:
            self.rect = self.image.get_rect(
            center=(
                currentX,currentY+(scrollY/4)
                )
            )
        self.rect.move_ip(self.speed, 0)
        if self.rect.left>SCREEN_WIDTH-60:
            self.speed *= -1
        if self.rect.right<60:
            self.speed *= -1
        


def characterSelection():
    global duck
    global dog
    duckImage = pygame.image.load("DuckSprite copy.png").convert()
    duckImage.set_colorkey((0, 0, 0), RLEACCEL)
    duckrect = duckImage.get_rect(midtop=(SCREEN_WIDTH//3, SCREEN_HEIGHT//2))
    
    dogImage = pygame.image.load("DogSprite copy.png").convert()
    dogImage.set_colorkey((0, 0, 0), RLEACCEL)
    dogrect = dogImage.get_rect(midtop=(2*SCREEN_WIDTH//3, SCREEN_HEIGHT//2))

    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if duckrect.collidepoint(event.pos):
                    duck = True
                    god = False
                    player1Selection()
                
                elif dogrect.collidepoint(event.pos):
                    duck = False
                    dog = True
                    player1Selection()
                    
        screen.fill((65,156,3))
        screen.blit(characterSelectImg,(0, 50))  
        screen.blit(duckImage,(SCREEN_WIDTH//3-35, SCREEN_HEIGHT//2))
        screen.blit(dogImage,(2*SCREEN_WIDTH//3-35, SCREEN_HEIGHT//2))
        pygame.display.update()

def characterSelection2():
    global duck
    global dog
    global singlePlayer
    global multiplayer
    global mouseClicks
    singlePlayer = False
    multiplayer = True
    duckImage = pygame.image.load("DuckSprite copy.png").convert()
    duckImage.set_colorkey((0, 0, 0), RLEACCEL)
    duckrect = duckImage.get_rect(midtop=(SCREEN_WIDTH//3, SCREEN_HEIGHT//2))
    
    dogImage = pygame.image.load("DogSprite copy.png").convert()
    dogImage.set_colorkey((0, 0, 0), RLEACCEL)
    dogrect = dogImage.get_rect(midtop=(2*SCREEN_WIDTH//3, SCREEN_HEIGHT//2))

    while True:
        screen.fill((65,156,3))
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if duckrect.collidepoint(event.pos):
                    mouseClicks += 1
                    if mouseClicks == 1:
                        player1TXT = "Player 1 is duck"
                        duck = True
                        dog = False
                        player1Selection()
                    else:
                        player2TXT = "Player 2 is duck"
                        duck = True
                        dog = False
                        draw_text(screen, player2TXT, 20, SCREEN_WIDTH//2, 565)
                        pygame.time.wait(1000)
                        player2Selection()
                
                elif dogrect.collidepoint(event.pos):
                    mouseClicks += 1
                    if mouseClicks == 1:
                        player1TXT = "Player 1 is dog"
                        duck = False
                        dog = True
                        player1Selection()
                    else:
                        player2TXT = "Player 2 is dog"
                        duck = False
                        dog = True
                        draw_text(screen, player2TXT, 20, SCREEN_WIDTH//2, 565)
                        pygame.time.wait(1000)
                        player2Selection()
                    
                
                    
        screen.fill((65,156,3))
        screen.blit(characterSelectImg,(0, 50))  
        screen.blit(duckImage,(SCREEN_WIDTH//3-35, SCREEN_HEIGHT//2))
        screen.blit(dogImage,(2*SCREEN_WIDTH//3-35, SCREEN_HEIGHT//2))
        if mouseClicks == 1:
            draw_text(screen, player1TXT, 20, SCREEN_WIDTH//2, 565)
        elif mouseClicks == 2:
            draw_text(screen, player2TXT, 20, SCREEN_WIDTH//2, 565)
        pygame.display.update()
        
POWERUP = pygame.USEREVENT + 6
        
class powerUp(pygame.sprite.Sprite):
    
    def __init__(self):
        super(powerUp,self).__init__()
        self.image = pygame.image.load("gemSprite.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.x = random.randint(10, SCREEN_WIDTH-10)
        self.rect = self.image.get_rect(
            center=(
                self.x,
                random.randint(0-scrollY, 700-scrollY),
                )
            )
        
    def update(self,pressed_keys):
        global player1
        global player2
        global poweredUp
        global poweredUp1
        global poweredUp2
        currentY = self.rect.y
        if pressed_keys[K_UP]:
            self.rect = self.image.get_rect(
            midtop=(
                self.x,currentY+(scrollY/4)
                )
            )
        if self.rect.top>SCREEN_HEIGHT:
            self.kill()
        if singlePlayer:
            col = pygame.sprite.collide_rect(self, player1)
            if col:
                self.kill()
                poweredUp = True
        if multiplayer:
            col = pygame.sprite.collide_rect(self, player1)
            col2 = pygame.sprite.collide_rect(self, player2)
            if col == True:
                poweredUp1 = True
                poweredUp2 = False
            if col2 == True:
                poweredUp1 = False
                poweredUp2 = True 

##OBSTACLES##

class Road(pygame.sprite.Sprite):
    global carOnRoadList
    
    def __init__(self,y):
        super(Road,self).__init__()
        self.image = pygame.image.load("roadPixel.png").convert()
        self.x = 300
        self.y = y
        self.rect = self.image.get_rect(center=(self.x,self.y+scrollY))
    
    def update(self,pressed_keys):
        global scrollY
        global roadOnScreen
        global counter
        if pressed_keys[K_UP] or pressed_keys[pygame.K_w]:
            #scrollY += 20
            self.rect = self.image.get_rect(
            center=(self.x,self.y+scrollY))
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()
            roadOnScreen = False
            counter -= 1
    
class cars(pygame.sprite.Sprite):
    
    def __init__(self,y):
        global scrollY
        super(cars,self).__init__()
        self.listOfCars = ["brown","blue","yellow"]
        self.color = random.choice(self.listOfCars)
        if self.color == "brown":
            self.image = pygame.image.load("brownCar.png").convert()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
        elif self.color == "blue":
            self.image = pygame.image.load("blueCar.png").convert()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
        elif self.color == "yellow":
            self.image = pygame.image.load("yellowCar.png").convert()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.x = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x,self.y+scrollY))
        self.speed = random.randint(5,20)
        
    def update(self,pressed_keys):
        global scrollY
        global roadOnScreen
        if pressed_keys[K_UP] or pressed_keys[pygame.K_w]:
            currentX = self.rect.x
            self.rect = self.image.get_rect(
            topleft=(currentX,self.y+scrollY))
        global carsOnScreen
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right<0:
            self.kill()
            carsOnScreen -= 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
            carsOnScreen -= 1

class River(pygame.sprite.Sprite):
    
    def __init__(self,y):
        global scrollY
        super(River,self).__init__()
        self.image = pygame.image.load("riverPixel.jpg").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.x = 0
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x,self.y+scrollY))
        
    def update(self,pressed_keys):
        global scrollY
        global counter
        if pressed_keys[K_UP] or pressed_keys[pygame.K_w]:
            self.rect = self.image.get_rect(
            topleft=(0,self.y+scrollY))
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()
            counter -= 1

class Bridge(pygame.sprite.Sprite):
    
    def __init__(self,y):
        global scrollY
        super(Bridge,self).__init__()
        self.x = random.randint(50,SCREEN_WIDTH-50)
        self.y = y
        self.image = pygame.image.load("bridge.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(midtop=(self.x,self.y+scrollY))
        self.speed = random.randrange(5,10)
    
    def update(self,pressed_keys):
        global scrollY
        if pressed_keys[K_UP] or pressed_keys[pygame.K_w]:
            currentX = self.rect.x
            self.rect = self.image.get_rect(
            topleft=(currentX,self.y+scrollY))
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right<90:
            self.speed *= -1
        if self.rect.left>SCREEN_WIDTH-90:
            self.speed *= -1
            
class Tracks(pygame.sprite.Sprite):
    
    def __init__(self,y):
        pass
    
def player1Selection():
    global duck
    global dog
    global player1
    global singlePlayer
    global multiplayer
    
    if duck == True:
        player1 = Duck() ##character selection
        all_sprites.add(player1)
        if singlePlayer:
            gameScreen()
        
    elif dog == True:
        player1 = Dog()
        all_sprites.add(player1)
        if singlePlayer:
            gameScreen()
            
def player2Selection():
    global duck
    global dog
    global player2
    
    if duck == True:
        player2 = Duck() ##character selection
        all_sprites.add(player2)
        gameScreen()
        
    elif dog == True:
        player2 = Dog()
        all_sprites.add(player2)
        gameScreen()
 
all_sprites = pygame.sprite.Group()
all_obstacles = pygame.sprite.Group()
all_bridges = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_powerups = pygame.sprite.Group()
score = 0
background = pygame.sprite.Group()
numberOfSteps = 0
listOfObstacles = ["car","train","river"]
obstaclesOnScreen = []
onBridge = False
ADDENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 10000)
ADDPOWERUP = pygame.USEREVENT + 7
pygame.time.set_timer(ADDPOWERUP, 5000)
POWERUPCOUNTDOWN = pygame.USEREVENT + 8



def gameScreen():
    global powerUpCounter
    enemyPresent = False
    global counter
    global onBridge
    global singlePlayer
    global multiplayer
    global poweredUp
    counter = 0
    while True:
        global score
        global carsOnScreen
        global roadOnScreen
        global scrollY
        global numberOfSteps
        global obstaclesOnScreen
        global riverOnScreen
        ADDCAR = pygame.USEREVENT + 1
        ADDRIVER = pygame.USEREVENT + 2
        listOfTimes = [500,1000]
        listOfDrawing = ["road","river"]
        timer = random.choice(listOfTimes)
        if numberOfSteps%5 == 0 and counter == 0:
                toDraw = random.choice(listOfDrawing)
                if toDraw == "road":
                    counter += 1
                    roadOnScreen = True
                    listOfTimes = [500,1000]
                    timer = random.choice(listOfTimes)
                    roadY = 50-scrollY
                    road = Road(50-scrollY)
                    pygame.time.set_timer(ADDCAR, timer)
                    all_sprites.add(road)
                if toDraw == "river":
                    bridgeY = random.randrange(-100,-75)
                    new_river = River(bridgeY-scrollY)
                    all_obstacles.add(new_river)
                    new_bridge = Bridge(bridgeY-scrollY-25)
                    all_bridges.add(new_bridge)
                    riverOnScreen = True
                    counter += 1

        die = True
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    menuScreen()
                if event.key == K_UP:
                    numberOfSteps += 1
            if event.type == ADDPOWERUP:
                gem = powerUp()
                all_powerups.add(gem)
            if event.type == POWERUPCOUNTDOWN and powerUpCounter>0:
                powerUpCounter -= 1
            if event.type == ADDENEMY:
                enemyPresent = True
                enemy = Enemy()
                all_enemies.add(enemy)
            if event.type == ADDCAR and carsOnScreen == 0 and roadOnScreen == True:
                new_car = cars(roadY+20)
                all_obstacles.add(new_car)
                carsOnScreen += 1
        
                               
        pressed_keys = pygame.key.get_pressed()
        
        all_obstacles.update(pressed_keys)
        
        if singlePlayer == True:
            player1.update(pressed_keys)
        else:
            player1.update(pressed_keys)
            player2.update(pressed_keys)
            
        all_obstacles.update(pressed_keys)
        all_sprites.update(pressed_keys)
        all_bridges.update(pressed_keys)
        all_enemies.update(pressed_keys)
        all_powerups.update(pressed_keys)
        
        screen.fill((65,156,3))
        
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        for obstacle in all_obstacles:
            screen.blit(obstacle.image, obstacle.rect)
        for bridges in all_bridges:
            screen.blit(bridges.image, bridges.rect)
        if riverOnScreen == True:
            screen.blit(new_river.image, new_river.rect)
            screen.blit(new_bridge.image, new_bridge.rect)
        for entity in all_enemies:
            screen.blit(entity.image, entity.rect)
        for powerup in all_powerups:
            screen.blit(powerup.image, powerup.rect)
    
            
        screen.blit(player1.image, player1.rect)
        if multiplayer:
            screen.blit(player1.image, player1.rect)
            screen.blit(player2.image, player2.rect)

        if singlePlayer:
            draw_text(screen, str(score//2), 18, SCREEN_WIDTH/6, 10)
            
        print(singlePlayer)
        
        if singlePlayer:
            if poweredUp:
                print("POWERUPPPP")
                powerUpCounter = 10
                pygame.time.set_timer(POWERUPCOUNTDOWN, 1000)
                
        if pygame.sprite.spritecollideany(player1, all_bridges):
            die = False
            onBridge = True
        
        if pygame.sprite.spritecollideany(player1, all_obstacles)  and die == True and singlePlayer == True and powerUpCounter == 0:
            player1.kill()
            running = False
            gameOverScreen()
        
        elif multiplayer and pygame.sprite.spritecollideany(player1, all_obstacles) and die == True and powerUpCounter1 == 0:
            player1.kill()
            running = False
            gameOverScreenPlayer1()
        
        elif multiplayer and pygame.sprite.spritecollideany(player2, all_obstacles) and die == True and powerUpCounter2 == 0:
            player2.kill()
            running = False
            gameOverScreenPlayer2()
            
            
        
        pygame.display.flip()
        
        clock.tick(10) ##fps


menuScreen()


