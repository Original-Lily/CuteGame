#Imports
import pygame
from pygame.locals import *
import sys
import random
import time

global NumbersToSort

display_frames = False
ran = 0
stored_score = 0
high_score = 0
NumbersToSort = []



def main_game():
    #Initialise PyGame 
    pygame.init()
    vec = pygame.math.Vector2 #2 for two dimensional
    #Setup size of window
    #normally H = 790, W = 400
    HEIGHT = 790
    WIDTH = 400
    #set player speed
    ACC = 0.5
    #Natural Friction
    FRIC = -0.12
    #Frames per second of the screen
    FPS = 60
    Pause_Length = 0
     
    FramePerSec = pygame.time.Clock()

    #Actually display window
    #(0, 0), pygame.RESIZABLE
    #(WIDTH, HEIGHT)
    #displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
    #Window Name
    pygame.display.set_caption("Game - A Level")

    #Setup player class values 
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.event.pump()
            super().__init__() 
            #??#self.image = pygame.image.load("character.png")
            #Create Player 'cube'
            self.surf = pygame.image.load(r"textures\CharacterCube.png")
            self.surf.set_alpha(255)
            self.rect = self.surf.get_rect()
            #Starting position
            #normally vec((10, 360))
            self.pos = vec((10, 750))
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.jumping = False
            #Set score to 0 before beginning 
            self.score = stored_score
            #set max number of double jumps
            self.double = False

            self.last = pygame.time.get_ticks()
            self.cooldown = 30
     
        def move(self):
            pygame.event.pump()
            #movement speed 
            self.acc = vec(0,0.5)
        
            pressed_keys = pygame.key.get_pressed()
            
            #Control direction depending on key press
            if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
            if pressed_keys[K_RIGHT]:
                self.acc.x = ACC

            #Basic Physics Engine
            #Combines the movement from player input alongside natural friction 
            self.acc.x += self.vel.x * FRIC
            #Controls velocity while moving
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            #??#Moves the objects 'centre' of mass; so to speak
            if self.pos.x > WIDTH:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = WIDTH
                 
            self.rect.midbottom = self.pos

        #Jump function
        def jump(self):
            #Detects for collision with a barrier/ Platform 
            hits = pygame.sprite.spritecollide(self, platforms, False)
            #If it touches a platform and is no longer 'Jumping' Place atop 
            if hits and not self.jumping:
               self.jumping = True
               self.vel.y = -15
            #check for double jump
            elif self.double == True:
                self.jumping = True
                self.vel.y = -15
                self.double = False
                    

        #Cancel jump function dictated by whether or not space is being held 
        def cancel_jump(self):
            #If you have cencelled the jump after jumping
            if self.jumping:
                #minus one from counter
                self.double == False
                #create a gravtity effect by setting the negative y acceleration via -3
                if self.vel.y < -3:
                    self.vel.y = -3

        #Updates every now and then to check for collision
        def update(self):
            global stored_score
            pygame.event.pump()
            #Detects collision
            hits = pygame.sprite.spritecollide(self ,platforms, False)
            #If you are travelling upwards 
            if self.vel.y > 0:
                #And if a collision with a platform is detected
                if hits:
                    #if the bottom of our character is touching the platform 
                    if self.pos.y < hits[0].rect.bottom:
                        #??#
                        if hits[0].point == True:
                            hits[0].point = False
                            # +1 to the score
                            self.score += 1
                            stored_score += 1
                            self.double = True
                        #??#
                        self.pos.y = hits[0].rect.top +1
                        self.vel.y = 0
                        #Reset jump function 
                        self.jumping = False

    #Create Platform function 
    class platform(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            #create platform of random width and always a height of 12 pixels
            self.surf = pygame.Surface(((random.randint(20,100)),12))
            #normally (random.randint((50,100),12))
            #Set platform colour to bright RGB green
            self.surf.fill((0,0,0))
            self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                     random.randint(0, HEIGHT-30)))
            platform_image = pygame.image.load(r"textures\Platform.png").convert()
            self.surf.blit(platform_image, [0, 0])
            self.surf.set_alpha(255)
            #Set the possible x-axis speed to a 33% chance of it either being traversing left, staying still or moving right
            self.speed = random.randint(-1, 1)
            #set moving variables to true
            self.moving = True
            self.point = True

        #Moving function setup
        def move(self):
            if self.moving == True:
                self.rect.move_ip(self.speed,0)
                if self.speed > 0 and self.rect.left > WIDTH:
                    self.rect.right = 0
                if self.speed < 0 and self.rect.right < 0:
                    self.rect.left = WIDTH
            PT1.moving = False
            PT1.point = False
            pass


     
    #Check for platform spawning
    def check(platform, groupies):
        if pygame.sprite.spritecollideany(platform,groupies):
            return True
        #If not
        else:
            #For every entity within the group
            for entity in groupies:
                #if said entity is a platform
                if entity == platform:
                    continue
                if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                    return True
            C = False

    #Platform Procedural generation control 
    def plat_gen():
        #While the number of platforms on screen is <10
        while len(platforms) < 10:
            width = random.randrange(50,100)
            p  = platform()      
            C = True
             
            while C:
                 p = platform()
                 p.rect.center = (random.randrange(0, WIDTH - width),
                                  random.randrange(-50, 0))
                 C = check(p, platforms)
            platforms.add(p)
            all_sprites.add(p)
     
    #Run platform and player functions 
    PT1 = platform()
    P1 = Player()

    #Create starting platform
    #Pick beginning platform's size
    PT1.surf = pygame.Surface((WIDTH, 20))
    Floor = pygame.image.load(r"textures\Floor.png").convert()
    PT1.surf.blit(Floor, [0, 0])
    #Generate it's colour via RGB values 
    #PT1.surf.fill((255,0,0))
    #Platform's dimensions 
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

    #Add sprites in the beginning
    all_sprites = pygame.sprite.Group()
    all_sprites.add(PT1)
    all_sprites.add(P1)

    #Include platforms
    platforms = pygame.sprite.Group()
    platforms.add(PT1)

    #Spawn in platforms
    for x in range(random.randint(6,12)):
        C = True
        pl = platform()
        while C:
            pl = platform()
            C = check(pl, platforms)
        platforms.add(pl)
        all_sprites.add(pl)
     
    #??#
    while True:
        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                global stored_score
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                pygame.display.update()
                time.sleep(1)
                text_file = open("Game_Scores.txt","a")
                text_file.write(str(stored_score)+"\n")
                #sortedfile = text_file(lines, key = lambda x : x[0])
                text_file.close()
                time.sleep(0.5)
                #text_file = open("Game_Scores","r")
                #print(text_file.read())
                #text_file.close
                pygame.quit()
                stored_score = 0
                #sys.exit()
                #main_game()
                menu()
        P1.update()
        try:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    menu()
                    #sys.exit()

                    
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_SPACE:
                        P1.jump()
                if event.type == pygame.KEYUP:    
                    if event.key == pygame.K_SPACE:
                        P1.cancel_jump()
                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.event.wait()
                            pygame.event.pump()
                            mainClock = pygame.time.Clock()
                            click = False
                            mopen = True
                            while mopen == True:
                                pygame.event.pump()
                                #set game clock (aka setting frame rate)
                                mainClock = pygame.time.Clock()
                                #function to determine what happens once the game button is selected 
                                def quick_game():
                                    running = True
                                    while running:
                                        pygame.quit()
                                        time.sleep(0.3)
                                        main_game()
                                #function to decide what the options button does
                                def quick_options():
                                    running = True
                                    #keydown event reactions 
                                    for event in pygame.event.get():
                                        if event.type == QUIT:
                                            try:
                                                pygame.quit()
                                                sys.exit()
                                            except:
                                                quit()
                                        if event.type == KEYDOWN:
                                            if event.key == K_ESCAPE:
                                                running = False
                                #create button variables to store shape, size and location 
                                qbutton_1 = pygame.Rect(50, 100, 200, 50)
                                qbutton_3 = pygame.Rect(50, 200, 200, 50)
                                #store position of the cursor (x,y)
                                qx, qy = pygame.mouse.get_pos()
                                #set what happens once you interact with a button
                                pygame.event.pump()
                                if qbutton_1.collidepoint((qx, qy)):
                                    if click:
                                        pygame.event.pump()
                                        mopen == False
                                        return()
                                if qbutton_3.collidepoint((qx, qy)):
                                    if click:
                                        pygame.quit()
                                        stored_score = 0
                                        menu()
                                #draw the buttons on screen, setting the colour and checking other aspects using the button variables
                                pygame.draw.rect(displaysurface, (200, 200, 200), qbutton_1)
                                pygame.draw.rect(displaysurface, (180, 180, 180), qbutton_3)
                                #setup other interactions without the use of a mouse 
                                click = False
                                #setup other interactions without the use of a mouse 
                                click = False
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        quit()
                                    if event.type == KEYDOWN:
                                        if event.key == K_ESCAPE:
                                            quit()
                                    if event.type == MOUSEBUTTONDOWN:
                                        if event.button == 1:
                                            click = True
                                pygame.event.pump()
                                #set the tick rate/ fps of the game
                                pygame.display.update()
                                mainClock.tick(60)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            quit()
            
        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

        #Run platform generation function 
        plat_gen()
        #Set screen background color
        displaysurface.fill((0,0,0))
        background_Platform = pygame.image.load(r"textures\Background.png").convert()
        displaysurface.blit(background_Platform, [0, 0])
        #Select the game's base font relative to pre-select sizes and styles 
        f = pygame.font.SysFont("Verdana", 20)
        #render the player's current score in the top center of the screen
        g = f.render(str(P1.score), True, (0,0,0))
        clock = pygame.time.Clock()

        def update_fps():
            frps = str(int(FramePerSec.tick()))
            frps_text = f.render(frps, 1, (0,0,0))
            return frps_text

        displaysurface.blit(g, (WIDTH/2, 10))
        if display_frames == True:
            ran = random.randint(1,100)
            if ran == 1:
                displaysurface.blit(update_fps(), (10,0))


        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        #Update the screen
        pygame.display.update()
        FramePerSec.tick(FPS)
    
#menu function 
def menu():
    global click
    #set game clock (aka setting frame rate)
    mainClock = pygame.time.Clock()
    #initialise pygame
    pygame.init()
    #generate display title
    pygame.display.set_caption('game base')
    #set display dimensions
    #(500, 500),0,32
    #(0, 0), pygame.FULLSCREEN for fullscreen
    #(0, 0), pygame.RESIZABLE for resizable window
    screen = pygame.display.set_mode((500, 500),0,32)
    
    #set game font
    font = pygame.font.SysFont("Verdana", 20)

    #function to create basic text at the top right of the screen 
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    click = False

    #menu page function
    def main_menu():
        while True:
            global click
            #set background colour
            #screen.fill((0,0,0))
            #set background image 
            background_image = pygame.image.load(r"textures\MenuBackground.png").convert()
            screen.blit(background_image, [0, 0])
            #create text saying 'main menu'
            #draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
            #store position of the cursor (x,y)
            mx, my = pygame.mouse.get_pos()
            #create button variables to store shape, size and location 
            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            button_3 = pygame.Rect(50, 300, 200, 50)
            #set what happens once you interact with a button
            pygame.event.pump()
            if button_1.collidepoint((mx, my)):
                if click:
                    try:
                        game()
                    except:
                        print("Oops!", sys.exc_info()[0], "occurred.")
                        main_menu()
            if button_2.collidepoint((mx, my)):
                if click:
                    options()
            if button_3.collidepoint((mx, my)):
                if click:
                    try:
                        pygame.quit()
                        sys.exit()
                    except:
                        quit()
            #draw the buttons on screen, setting the colour and checking other aspects using the button variables
            pygame.draw.rect(screen, (0, 255, 0), button_1)
            pygame.draw.rect(screen, (0, 255, 0), button_2)
            pygame.draw.rect(screen, (255, 0, 0), button_3)
            #give icon images
            scoreImage = pygame.image.load(r"textures\Clickable1.png").convert()
            scoreImage2 = pygame.image.load(r"textures\Clickable2.png").convert()
            screen.blit(scoreImage, [50,100])
            screen.blit(scoreImage2, [50,200])
            screen.blit(scoreImage, [50,300])
            #give names to buttons
            draw_text('Play', font, (255, 255, 255), screen, 60, 110)
            draw_text('Options', font, (255, 255, 255), screen, 60, 210)
            draw_text('Exit Game', font, (255, 255, 255), screen, 60, 310)
            #setup other interactions without the use of a mouse 
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            #set the tick rate/ fps of the game
            pygame.display.update()
            mainClock.tick(60)
    #function to determine what happens once the game button is selected 
    def game():
        running = True
        while running:
            pygame.event.pump()
            pygame.quit()
            try:
                main_game()
            except:
                game()
                
    def score_display():
        global display_frames
        toSort = open("Game_Scores.txt","r+")
        NumbersToSort = sorted(list(map(int, toSort.readlines())))
        NumbersToSort.sort(reverse=True)
        running = True
        while running:
            global click
            #set new background image 
            background_image = pygame.image.load(r"textures\MenuBackground.png").convert()
            screen.blit(background_image, [0, 0])
            #set 'backup' background colour 
            #screen.fill((0,0,0))
            mx, my = pygame.mouse.get_pos()
            score1 = pygame.Rect(50, 100, 100, 50)
            score2 = pygame.Rect(50, 200, 100, 50)
            score3 = pygame.Rect(50, 300, 100, 50)
            score4 = pygame.Rect(250, 100, 100, 50)
            score5 = pygame.Rect(250, 200, 100, 50)
            score6 = pygame.Rect(250, 300, 100, 50)
            exit_button = pygame.Rect(400, 450, 100, 50)
            #draw rectangles
            pygame.draw.rect(screen, (0, 255, 0), score1)
            pygame.draw.rect(screen, (0, 255, 0), score2)
            pygame.draw.rect(screen, (0, 255, 0), score3)
            pygame.draw.rect(screen, (0, 255, 0), score4)
            pygame.draw.rect(screen, (0, 255, 0), score5)
            pygame.draw.rect(screen, (0, 255, 0), score6)
            pygame.draw.rect(screen, (255, 0, 0), exit_button)
            #give images
            scoreImage = pygame.image.load(r"textures\SmallClickable1.png").convert()
            scoreImage2 = pygame.image.load(r"textures\SmallClickable2.png").convert()
            screen.blit(scoreImage, [50,100])
            screen.blit(scoreImage2, [50,200])
            screen.blit(scoreImage, [50,300])
            screen.blit(scoreImage, [250,100])
            screen.blit(scoreImage2, [250,200])
            screen.blit(scoreImage2, [250,300])
            screen.blit(scoreImage2, [400,450])
            #draw_text('Latest Scores', font, (255, 255, 255), screen, 20, 10)
            draw_text('Back', font, (255, 255, 255), screen, 410, 460)
            text_file = open("Game_Scores.txt","r")
            draw_text(str(NumbersToSort[0]), font, (255, 255, 255), screen, 50, 100)
            draw_text(str(NumbersToSort[1]), font, (255, 255, 255), screen, 50, 200)
            draw_text(str(NumbersToSort[2]), font, (255, 255, 255), screen, 50, 300)
            draw_text(str(NumbersToSort[3]), font, (255, 255, 255), screen, 250, 100)
            draw_text(str(NumbersToSort[4]), font, (255, 255, 255), screen, 250, 200)
            draw_text(str(NumbersToSort[5]), font, (255, 255, 255), screen, 250, 300)
            text_file.close
            pygame.event.pump()
            if exit_button.collidepoint((mx,my)):
                if click:
                    pygame.draw.rect(screen, (0, 255, 0), exit_button)
                    options()

            #setup other interactions without the use of a mouse 
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            #set the tick rate/ fps of the game
            pygame.display.update()
            mainClock.tick(60)
                
    #function to decide what the options button does
    def options():
        global display_frames
        running = True
        while running:
            global click
            #set new background image 
            background_image = pygame.image.load(r"textures\MenuBackground.png").convert()
            screen.blit(background_image, [0, 0])
            #set 'backup' background colour 
            #screen.fill((0,0,0))
            mx, my = pygame.mouse.get_pos()
            button_a = pygame.Rect(250, 100, 200, 50)
            button_c = pygame.Rect(250, 200, 200, 50)
            button_b = pygame.Rect(250, 300, 200, 50)
            #draw relative to top right of the screen
            pygame.draw.rect(screen, (0, 255, 0), button_a)
            pygame.draw.rect(screen, (0, 255, 0), button_c)
            pygame.draw.rect(screen, (255, 0, 0), button_b)
            #give icon images
            scoreImage = pygame.image.load(r"textures\Clickable1.png").convert()
            scoreImage2 = pygame.image.load(r"textures\Clickable2.png").convert()
            screen.blit(scoreImage, [250,100])
            screen.blit(scoreImage2, [250,200])
            screen.blit(scoreImage2, [250,300])
            #give text
            #draw_text('Options', font, (255, 255, 255), screen, 20, 20)
            draw_text('FPS Toggle', font, (255, 255, 255), screen, 260, 110)
            draw_text('Scoreboard', font, (255, 255, 255), screen, 260, 210)
            draw_text('Back', font, (255, 255, 255), screen, 260, 310)
            pygame.event.pump()
            if button_a.collidepoint((mx, my)):
                if click:
                    if display_frames == False:
                        display_frames = True
                        pygame.draw.rect(screen, (255, 0, 0), button_a)
                    else:
                        display_frames = False
                        pygame.draw.rect(screen, (255, 0, 0), button_a)
            if button_b.collidepoint((mx, my)):
                if click:
                    main_menu()
            if button_c.collidepoint((mx, my)):
                if click:
                    pygame.draw.rect(screen, (255, 0, 0), button_c)
                    score_display()
                    
            #setup other interactions without the use of a mouse 
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            #set the tick rate/ fps of the game
            pygame.display.update()
            mainClock.tick(60)
            
            #keydown event reactions 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            #set the tick rate/ fps of the game
            pygame.display.update()
            mainClock.tick(60)

    main_menu()

global click
menu()
#end of game



