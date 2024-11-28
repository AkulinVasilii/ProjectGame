import pygame
import os
from bullet import *
import random
img_dir = os.path.join(os.path.dirname(__file__), 'graphics_forgame')
snd_dir = os.path.join(os.path.dirname(__file__), 'sound_game')
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 600
HEIGHT = 750
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# loading sound effects
# sound of shoot
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'laser_gun.wav'))
# loading graphics for player's and fighter's sprites
player_img = pygame.image.load(os.path.join(img_dir, "x-wing.png")).convert()
fighter_img = pygame.image.load(os.path.join(img_dir, "fighter of Empire.png")).convert()
# sprite of player
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# create class for observing the player's laser gun's hits
class Player(pygame.sprite.Sprite):
    # initialisation
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        
    # drawing per iteration
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    # method for player's shooting        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        shoot_sound.play()
        return bullet
    
 
# sprite of the comets and fighters
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = fighter_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(fighter_img, (35, 35))
        self.rect = self.image.get_rect()
        self.radius = 15
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)    