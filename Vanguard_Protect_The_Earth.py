#Author: Victor G. Balcazar
#Contact Info: victorbalcazar3@hotmail.com
#Class: CPSC 386 - Project 5
#Title: Vanguard Protect the Earth! (project 5)
#Resources Used:
#   KidsCanCode video series. Retrieved from: https://www.youtube.com/channel/UCNaPQ5uLX5iIEHUCLmfAgKg
#   Sources from Open Game Art . org:
#       SHMUP SHIPS by surt. Retrieved from: http://opengameart.org/content/shmup-ships
#       through space by maxstack. Retrieved from: http://opengameart.org/content/through-space
#       bullet collection 1 m484 by Master484. Retrieved from: http://opengameart.org/content/bullet-collection-1-m484
#       explosion set 1 m484 by Master484. Retrieced from: http://opengameart.org/content/explosion-set-1-m484-games
#   Laser and explosion sound effects generated using: http://www.bfxr.net/
#   Space Background by kidscancode. Retrieved from: http://imgur.com/bHiPMju

#Game Description: A classic arcade-y shoot em up. There's a ship at the bottom of the screen, you press space bar to shoot asteroids and
#enemy ships while avoiding the ones you can't shoot down. The game opens with a title screen, this serves as both the main "menu" and
#"game over" screen. Within the menu screen the player only has two options: press the window x to exit, or press any keyboard key to 
#start the game. In the main game you have you ship on the bottom of the screen, you can only move left or right. You can press the space
#bar to fire bullets. On the top left you have your lives, represented by little sprites in the shape of your ship, whenever you are hit 
#one will disapear from the right until you reach zero lives at which moment an animation of your ship exploding and a command will take you
#back to the menu screen, this is the game over state. On the top center of the game screen there is a number that increases when you destroy
#enemies, this is your score, it doesn't transfer over, nor is it recorded. The point of the game is to see how far you can go without dying.
#There are two types of enemies. The asteroids which appear in waves so long as there doesn't exist more than 10, meaning that there will 
#always be at least 9 asteroids on screen. The biggest asteroid requires two bullets to destroy. The other kind of enemy is the green enemy
#ships that fire green bullets which are slower than the player's bullets. The enemy ships move horizontally and won't come down to attack
#the player. Enemy ships require two bullets to kill. When the player kills an enemy they are rewarded with some points for their score
#and these points are based on the radius of the asteroids, the biggest ones are worth less than the smaller ones. The ships are worth
#a set amount.
#Each sprite on screen has its own class. There is one game loop. sound effects for enemy fire and player bullets. One looping music track.
#Two animations for when an enemy is destroyed and one for when the player dies.
#The game creates a certain number of enemies in timed intervals up to a cap, preventing the player from become too overwhelmed. There is an
#interval at the beginning of each game where there are no enemies, this is to let the player quickly get a feel for the controls. Asteroids
#appear first and tackle the player. By themselves they are not much of a threat. But after the "adjusting period" the enemy ships appear 
#and shoot at the player, this makes the game much harder, but the player had enough time to adjust to the change in pace. To further help
#this adjusting peroid the player is given 5 lives instead of the traditional 3 lives. The player moves at a speed that is not too fast as
#to make the player more likely to accidentally hit a slow asteroid and the like and not so slow that the player can't maneuver through
#the potential bullet hell.

import pygame
import random
import os
import sys

#######################INITIALIZATION################################################################
#these allow for easier calling of images from their respective folders
img_dir = os.path.join(os.path.dirname('__file__'), 'images')
snd_dir = os.path.join(os.path.dirname('__file__'), 'snd')
#screen width and height, important to set up so they can be manipulated throughout the program
WIDTH = 550
HEIGHT = 700
FPS = 60 #rate at which I wish for the screen to update, 60 frams per second.

#initialize Pygame and Create the Window+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#function for making text appear on screen+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
fontName = pygame.font.match_font('arial')
def draw_text(surface, msg, size, x, y):
    font = pygame.font.Font(fontName, size)
    text_surface = font.render(msg, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)
#TIMED EVENTS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
TIME_TILL_ENEMIES = 3000 #intervall for the asteroids to appear
TIME_TILL_ENEMIES2 = 6500 #intervall for the enemy ships to appear

ADJUSTING_PERIOD = 12000 #time before the enemy ships start appearing, this creates a more difficult game
#user defined events
make_Enemies1 = pygame.USEREVENT +1
make_Enemies2 = pygame.USEREVENT +2
#these set the intervals at which events are generated
pygame.time.set_timer(make_Enemies1, TIME_TILL_ENEMIES)
pygame.time.set_timer(make_Enemies2, TIME_TILL_ENEMIES2)

#Define Colors+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)
ORANGE = (250,110,0) 

#load images+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
background = pygame.image.load(os.path.join(img_dir, "space_bg.png")).convert()
background = pygame.transform.scale(background, (550,700))
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir, "human_ship.png")).convert()
player_img_rect = player_img.get_rect()
asteroid1_img = pygame.image.load(os.path.join(img_dir, "asteroid_1.png")).convert()
enemy_ship = pygame.image.load(os.path.join(img_dir, "enemy_ship_1.png")).convert()
enemy_ship_rect = enemy_ship.get_rect()
player_fire_img = pygame.image.load(os.path.join(img_dir, "player_fire.png")).convert()
enemy_fire_img = pygame.image.load(os.path.join(img_dir, "enemy_fire.png")).convert()

asteroid_images = []
asteroid_list = ['asteroid_3.png', 'asteroid_1.png', 'asteroid_2.png']

for img in asteroid_list:
    asteroid_images.append(pygame.image.load(os.path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['bs'] = []
explosion_anim['Ts'] = []
for i in range(7):
    filename = 'bang{}.png'.format(i)
    filename2 = 'boom{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img2 = pygame.image.load(os.path.join(img_dir, filename2)).convert()
    img2.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (40,40))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (25,25))
    explosion_anim['sm'].append(img_sm)
    img_bs = pygame.transform.scale(img2, (60,60))
    explosion_anim['bs'].append(img_bs)
    img_Ts = pygame.transform.scale(img2, (100,100))
    explosion_anim['Ts'].append(img_Ts)

#Load Sounds+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
p_shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot7.wav'))
pygame.mixer.Sound.set_volume(p_shoot_sound, .3)
e_shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot.wav'))
explosion_s = pygame.mixer.Sound(os.path.join(snd_dir, 'Explosion3.wav'))
explosion_s2 = pygame.mixer.Sound(os.path.join(snd_dir, 'Explosion4.wav'))
playerHit = pygame.mixer.Sound(os.path.join(snd_dir, 'playerHit.wav'))
pygame.mixer.Sound.set_volume(playerHit, 1)
pygame.mixer.music.load(os.path.join(snd_dir, 'through_space.wav'))
pygame.mixer.music.set_volume(1.6)
##################END OF INITIALIZATION##################################################################

##################CLASSES################################################################################
#player class ===========================================================================================
class Player(pygame.sprite.Sprite):
    """This is the player class. When initialized it has five lives and appears at the bottom center of the screen. An internal radius
    is used to determine collisions between the player sprite and asteroids or bullets. It has an update function that tells pygame to 
    make the ship move or stay put if the player presses the left and right arrow keys. It also calls the class' shoot function if 
    it the player presses the space bar. the shoot function creates a Bullet class object and puts in the front center of the player's
    ship. The hide function serves to move the ship from the player's sight while the player death explosion animation occurs."""
    #player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (45,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 24
        self.life = 5
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 130
        self.last_shot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()


    def update(self):

        #are we hidden?
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: #a cheap way to get rid of the player without destroying it
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx =-6
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
        self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self. rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            p_shoot_sound.play()
    def hide(self):
        """hide the player temporarily"""
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+100)

#enemy1: asteroid class==================================================================================
class Enemy1(pygame.sprite.Sprite):
    """This is the asteroid class. it randomly chooses from a collection of three asteroid images. When the image chosen is the one with
    the largest internal radius it is given 2 lives. The asteroids are created above the game screen and outside the players perception.
    From there they move downwards and if they hit the horizontal walls their horizontal speed is reversed so they reapear on screen. If
    they reach the end of the vertal boundaries of the screen they are moved to the top so they can continue to be obstacles to the player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(asteroid_images)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.9/2)
        if self.radius > 15:
            self.life = 2
        else:
            self.life = 1
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -40)
        self.speedy = random.randrange(2, 6)
        self.speedx = random.randrange(-1,2)
        

    def update(self):
        if self.life < 1:
            self.kill()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)
        if self.speedx > 0:
            if self.rect.right > WIDTH + 10:
                self.speedx = (-1*self.speedx)
                self.bounce = True

            elif self.rect.right < -10 and self.bounce:
                self.speedx = (-1*self.speedx)
        else:
            if self.rect.right > WIDTH + 10 and self.bounce:
                self.speedx = (-1*self.speedx)
            elif self.rect.right < -10:
                self.speedx = (-1*self.speedx)
                self.bounce = True
        
#enemy2: enemy ships class================================================================================
class Enemy2(pygame.sprite.Sprite):#The ones that come from the sides
    """This is the enemy ship class. Similarly to the asteroid it creates an enemy that moves on the screen. This enemy appears from the 
    horizontal plan and will never appear bellow the vertical mid section of the game screen. It moves back and forward horizontally and
    shoots bullets at random intervals. The intervals where determined with constant testing and the option chosen was deemed fair. The 
    Enemy ships and bullets are bright green so they are easy to spot and don't get lost among the asteroids. They take two shoots to die.
    Enemy bullets are modified inside the shoot function of this class."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_ship
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.life = 2
        self.rect.x = random.randrange(-100, -40)
        self.rect.y = random.randrange((HEIGHT/2) - self.rect.width)
        self.speedx = random.randrange(1, 3)
        
        self.bounce = False
        self.last_time_shot = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        tmp_random = random.randrange(1400, 2000)
        if now - self.last_time_shot > tmp_random:
            self.last_time_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom)
            bullet.image = pygame.transform.scale(enemy_fire_img, (8,15))
            bullet.image.set_colorkey(BLACK)
            bullet.speedy = 2
            bullet.radius = 1
            all_sprites.add(bullet)
            ebullets.add(bullet)
            e_shoot_sound.play()

    def update(self):
        self.rect.x += self.speedx
        if self.life < 1 :
            self.kill()
        if self.speedx > 0:
            if self.rect.right > WIDTH + 10:
                self.speedx = (-1*self.speedx)
                self.bounce = True

            elif self.rect.right < -10 and self.bounce:
                self.speedx = (-1*self.speedx)
        else:
            if self.rect.right > WIDTH + 10 and self.bounce:
                self.speedx = (-1*self.speedx)

            elif self.rect.right < -10:
                self.speedx = (-1*self.speedx)
                self.bounce = True
        self.shoot()
#Bullet class=============================================================================================
class Bullet(pygame.sprite.Sprite):
    """This is teh Bullet class, it creates a bullet sprite in front of that is given. The enemy bullets are modified in the shoot function
    of the enemy ships. They travel vertically and disapear when they reach the bottom of top of the screen"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_fire_img, (8,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 1
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 0
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #kill them all peter or, kill yo' self
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
class PlayerLifeSprite(pygame.sprite.Sprite):
    """This is just a sprite class thats a small ship sprite appear where designated. It is nothing special"""
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (15,20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    #def update(self):
class Explosion(pygame.sprite.Sprite):
    """This is the Explosion animation class. It animates an explosion at the given coordinates and the explosion depends of the two character
    command given under 'size' which is the name of a directory containing the images neccesary. At the end of the animation it terminates 
    itself."""
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 70

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
###########################END OF CLASSES#################################################################
#FUNCTION DEFINITIONS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.display.set_caption("Vanguard Protect The Earth!!!")
clock = pygame.time.Clock()
"""This function adds the number of player lives sprites onto the screen. The group pLifesG is emptied at the beginning of the function
in order to prevent the computer from having to compute more sprites than necessary"""
def drawPlayerLife(pLife):
    pLifesG.empty()
    for i in xrange (pLife):
        m = PlayerLifeSprite(10 + (15*i), 20)
        pLifesG.add(m)
"""This function makes an asteroid at the top of the screen and adds it to the all sprites group and the enemies1 group, which is the
asteroid group."""
def createEnemy1():
    m = Enemy1()
    all_sprites.add(m)
    enemies1.add(m)
"""This function generates a number from 1 to 50 and if larger than 25 the enemy will spawn from the left and it will be added to the
all sprites group and the enemies2 group, the designated enemy ship group. if below 25 it spawns an enemy ship from the right and changes
its horizontal speed to it travels right and  will be added to the all sprites group and the enemies2 group"""
def createEnemy2():
    leftOrRight = random.randrange(1,50)
    if leftOrRight > 25:
        m = Enemy2()

        all_sprites.add(m)
        enemies2.add(m)
    else:
        m = Enemy2()
        m.speedx = m.speedx * -1
        m.rect.x = ((m.rect.x * -1) + WIDTH)
        all_sprites.add(m)
        enemies2.add(m)
"""This creates the start menu/game over screen. Text appears onscreen giving the title of the game, Vanguard as well as the instructinos
on how to play the game. It also tells the player to press any key to play the game. The only other option from this screen is to exit the 
game via the x button on the window. """
def showGOScreen():
    screen.blit(background, background_rect)
    draw_text(screen, "Vanguard!", 74, WIDTH /2, HEIGHT/4 )
    draw_text(screen, "Arrow keys to move, Space Bar to Shoot", 30, WIDTH/2, HEIGHT/2)

    draw_text(screen, "Press any key to Start", 50, WIDTH/2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #done = True
            if event.type == pygame.KEYUP:
                waiting = False
                keep_of_time = pygame.time.get_ticks()
#Make Background Music Play================================================================================
pygame.mixer.music.play(loops = -1)

#######################FUNCTION DEFINITIONS END############################################################

#######################MAIN GAME LOOP START################################################################
#Game Loop=================================================================================================
done = True #tell whether the main game loop should continue or no
gameOver = True #are we at the game over screen?
while done:
    #initial state of game: Game Start/Over screen
    """Game always starts at the menu/game over screen"""
    if gameOver:
        showGOScreen()
        """Once the player presses a key to exit the screen the groups and player sprite are initialized. The enemies are kept in check with
        timed events handled in the event handling section. It also sets the player score to 0."""
        gameOver = False
        score = 0 #keeps player score

        all_sprites = pygame.sprite.Group()
        enemies1 = pygame.sprite.Group()
        enemies2 = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        ebullets = pygame.sprite.Group()
        pLifesG = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        keep_of_time = pygame.time.get_ticks() #this helps keep track of when the screen is changed to the game screen
    #run at desired speed==============================================================================
    clock.tick(FPS)
    #Events============================================================================================
    """This keeps track of time and when enemies have to spawn, but it will only do so when the game over screen is no longer active.
    It also checks whether the player decides to exit the program."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == make_Enemies1 and gameOver == False and ((pygame.time.get_ticks() - keep_of_time) > 3000):
            print "Hey I work"
            if len(enemies1) < 10:
                for i in range(15):
                    createEnemy1()
        elif event.type == make_Enemies2 and gameOver == False and ((pygame.time.get_ticks() - keep_of_time) > 9500):
            print "Hey I work2"
            if len(enemies2) < 6 and pygame.time.get_ticks() > ADJUSTING_PERIOD:
                for i in range(5):
                    createEnemy2()
    #Update objects======================================================================================
    
    all_sprites.update() # this calls the update function on each sprite class
    #check if Enemies hit player
    hits_E1 = pygame.sprite.spritecollide(player, enemies1, True, pygame.sprite.collide_circle)
    for hit in hits_E1:
        player.life -= 1 #reduces player life when there is a collision between the player and an asteroid
        playerHit.play() #plays the sound effect
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.life <=0: #When player lifes run out it plays teh explosion for the player 'Ts'
            pexpl = Explosion(player.rect.center, 'Ts')
            all_sprites.add(pexpl)
            player.hide()
            explosion_s2.play()
            
        #if player died and explosion finished
    if  player.life <= 0 and not pexpl.alive(): #when the player explosion ends the game over screen is called back
        gameOver = True
    #check if player bullet hits asteroid
    hits = pygame.sprite.groupcollide(enemies1, bullets, False, True)
    for hit in hits:
        hit.life -= 1
        if hit.life < 1:
            score += 50 - hit.radius
            explosion_s.play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
    #check if player bullet hits enemy ship
    hits2 = pygame.sprite.groupcollide(enemies2, bullets, False, True)
    for hit in hits2:
        hit.life -= 1
        if hit.life < 1:
            score += 30
            explosion_s2.play()
            expl = Explosion(hit.rect.center, 'bs')
            all_sprites.add(expl)
    drawPlayerLife(player.life)
    #check if enemy bullets hit player
    hits3 = pygame.sprite.spritecollide(player, ebullets, True, pygame.sprite.collide_circle)
    for hit in hits3:
        player.life -= 1
        playerHit.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.life <=0:
            explosion_s2.play()
            pexpl = Explosion(player.rect.center, 'Ts')
            all_sprites.add(pexpl)
            player.hide()
    if  player.life <= 0 and not pexpl.alive(): #when the player explosion ends the game over screen is called back
        gameOver = True

    #Rendering Stuff
    screen.fill(BLACK)
    screen.blit(background, background_rect) #load background to screen
    all_sprites.draw(screen) #draws all sprites group to screen
    pLifesG.draw(screen) #draws all player lives sprites to the screen
    draw_text(screen, str(score), 18, WIDTH/2, 10) #displays the player's current score.
    pygame.display.flip()
#################END OF GAME LOOP####################################################################################
pygame.quit()
sys.exit()

