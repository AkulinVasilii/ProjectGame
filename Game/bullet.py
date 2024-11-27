import pygame
import os
img_dir = os.path.join(os.path.dirname(__file__), 'graphics_forgame')
snd_dir = os.path.join(os.path.dirname(__file__), 'sound_game')
BLACK = (0, 0, 0)

WIDTH = 600
HEIGHT = 750
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
bullet_img = pygame.image.load(os.path.join(img_dir, "laserGreen.png")).convert()
# create class for observing the player's laser gun's hits
class Bullet(pygame.sprite.Sprite):
    # class initialisation
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(bullet_img, (5, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    # bullet control
    def update(self):
        self.rect.y += self.speedy
        # delete whether it out of screen
        if self.rect.bottom < 0:
            self.kill()