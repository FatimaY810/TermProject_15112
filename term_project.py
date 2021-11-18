import pygame
import random
### future implements:
# character selection
# multiplayer (WASD)

score = 0
scrollY = 0
carsOnScreen = 0
roadOnScreen = False

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
        self.playerIMGRight = [] #duck sprite facing right
        self.playerIMGLeft = []
        self.walk1 = pygame.image.load("DuckWalk1.png").convert()
        self.walk1.set_colorkey((0, 0, 0), RLEACCEL) ##render each image to get rid of the black background
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
      
        self.rect = self.image.get_rect(topleft=(225,750))
        ##grabs rectangle attributes from rect class
        
    def update(self,pressed_keys):
        global scrollY
        ##moving the sprite
        if pressed_keys[K_UP]:
            scrollY -= 5
            self.indexRight = 0
            self.indexLeft = 0
            self.indexUp += 1
            i = self.indexUp-1
            self.image = self.playerIMG[i]
            if self.indexUp >=5:
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
            
            
        ##keeping it on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 750
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

##OBSTACLES##
class Road(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Road,self).__init__()
        self.scrollY = 0
        self.image = pygame.image.load("roadPixel.png").convert()
        self.x = 300
        self.y = 50
        self.rect = self.image.get_rect(center=(self.x,self.y+scrollY))
    
    def update(self,pressed_keys):
        global scrollY
        global roadOnScreen
        if pressed_keys[K_UP]:
            scrollY += 20
            self.rect = self.image.get_rect(
            topleft=(self.x,self.y+scrollY))
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
            roadOnScreen = False
            
            
class cars(pygame.sprite.Sprite):
    
    def __init__(self):
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
        self.y = 50
        self.rect = self.image.get_rect(center=(self.x,self.y+scrollY))
        self.speed = random.randint(5,20)
    def update(self,pressed_keys):
        global scrollY
        global roadOnScreen
        if pressed_keys[K_UP]:
            scrollY += 10
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
            roadOnScreen = False

class River(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super(River,self).__init__()
        self.scrollY = 0
        self.image = pygame.image.load("riverPixel.png").convert()
        self.x = 0
        self.y = random.randint(100,400)
        self.rect = self.image.get_rect(topleft=(self.x,self.y+scrollY))
        
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            scrollY += 6
            self.rect = self.image.get_rect(
            center=(0,self.y+scrollY))
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()

class Bridge(River):
    
    def __init__(self,x,y):
        super(Bridge,self).__init__()
        super().__init__(y)
        self.x = random.randint(50,SCREEN_WIDTH-50)
        self.scrollY = 0
        self.image = pygame.image.load("bridge.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(topleft=(self.x,self.y+scrollY))
    
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            scrollY += 6
            self.rect = self.image.get_rect(
            center=(0,self.y+scrollY))
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
            
player1 = Player()
all_sprites = pygame.sprite.Group()
all_obstacles = pygame.sprite.Group()
all_sprites.add(player1)
score = 0
background = pygame.sprite.Group()
numberOfSteps = 0
listOfObstacles = ["car","train","river"]

def gameScreen():
    global carsOnScreen
    global roadOnScreen
    global scrollY
    global numberOfSteps
    ADDCAR = pygame.USEREVENT + 1
    ADDRIVER = pygame.USEREVENT + 2
    listOfTimes = [500,1000]
    timer = random.choice(listOfTimes)
    pygame.time.set_timer(ADDCAR, timer)
    while True:
        if numberOfSteps%10 == 0:
            print("hello")
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()
                if event.key == K_UP:
                    print("moved up")
                    numberOfSteps += 1
            if event.type == ADDCAR and carsOnScreen == 0:
                roadOnScreen = True
                road = Road()
                all_sprites.add(road)
                new_car = cars()
                all_obstacles.add(new_car)
                carsOnScreen += 1
            if event.type == ADDRIVER:
                new_river = River()
                all_obstacles.add(new_river)
                new_bridge = Bridge()
                all_sprites.add(new_bridge)
        
        print("here is the number", numberOfSteps)
                       
        pressed_keys = pygame.key.get_pressed()
        
        all_obstacles.update(pressed_keys)
        
        player1.update(pressed_keys)
        all_obstacles.update(pressed_keys)
        
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        for obstacle in all_obstacles:
            screen.blit(obstacle.image, obstacle.rect)
            
                
        screen.fill((65,156,3))
        
        all_sprites.draw(screen)
        all_obstacles.draw(screen)
        
        if pygame.sprite.spritecollideany(player1, all_obstacles):
            player1.kill()
            running = False
            pygame.quit()
            quit()
        
        pygame.display.flip()
        
        clock.tick(15) ##fps
            
print(scrollY)       
menuScreen()
