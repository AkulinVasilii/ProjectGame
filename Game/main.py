import os
# available path to directory
img_dir = os.path.join(os.path.dirname(__file__), 'graphics_forgame')
snd_dir = os.path.join(os.path.dirname(__file__), 'sound_game')
import pygame
from bullet import *
from player_and_mob import *
from def_drawtext import draw_text
from file_worker import *
WIDTH = 600
HEIGHT = 750
FPS = 90

# Imagine the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Start the game and creation of a screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# loading sound effects
# sound of shoot
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'laser_gun.wav'))
# sounds of explosions
expl_sounds = []
for snd in ['space_expl1.wav', 'space_expl2.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, snd)))
# movement sound effects
move_sounds = []
for move in ['manevr1.wav', 'manevr2.wav']:
    move_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir, move)))
#loading music
pygame.mixer.music.load(os.path.join(snd_dir, 'music.mp3'))
pygame.mixer.music.set_volume(1)

# loading background
background = pygame.image.load(os.path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
# loading graphics for player, fighter and bullets sprite
player_img = pygame.image.load(os.path.join(img_dir, "x-wing.png")).convert()
fighter_img = pygame.image.load(os.path.join(img_dir, "fighter of Empire.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, "laserGreen.png")).convert()

#showing start screen            
def show_go_screen():
    cur_name = 'Guest'
    iwriter('cur_name.txt', cur_name)
    need_input = False
    input_text = '' 
    waiting = True
    flag_game = True
    while waiting:
        clock.tick(FPS)
# starting menu with opportunity to create a profile
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_game = False
                waiting = False
                return flag_game
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    waiting = False
                    return flag_game
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    need_input = False
                    name = input_text
                    iwriter('cur_name.txt', name)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text)<10:
                        input_text += event.unicode  
        if flag_game:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                need_input = True 
# drawing start screen    
            screen.blit(background, background_rect)
            draw_text(screen, "STAR WARS", 64, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, "Press RSHIFT to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
            draw_text(screen, input_text, 32, WIDTH/2, HEIGHT/2)
            pygame.display.flip()
        
            
# install a timer
clock = pygame.time.Clock()
# create groups of sprites
score = 0
max_game_score = int(ireader('best_score.txt'))
pygame.mixer.music.play(loops=-1)

# Main loop of game
running = True
game_over = True
while running:
    if game_over:
        flag_game = show_go_screen()
        game_over = False
# create groups of sprites
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        mobs = pygame.sprite.Group()
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        bullets = pygame.sprite.Group()
        score = 0
    # keeping loop on correct speed
    clock.tick(FPS)
    if not flag_game:
        running = False
        break
    else:
# input of process(event)
        for event in pygame.event.get():
# check for closing window
            if event.type == pygame.QUIT:
                running = False
# check the player's movement    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                    move_sounds[0].play()
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                    move_sounds[1].play()
# check the player's shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)
# update all of the objects
        all_sprites.update()
# checking if player faces with something
        hits_npc = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits_npc:
# checking if player beats the record score
            if max_game_score < score:
                max_game_score = score
                name = ireader('cur_name.txt')
                iwriter('best_player_name.txt', name)
                iwriter('best_score.txt', str(max_game_score))
            game_over = True
# check if player gets to fighter
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 1
            m = Mob()
            expl_sounds[0].play()
            all_sprites.add(m)
            mobs.add(m)
# Rendering screen
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        out = open('cur_name.txt', )
        draw_text(screen, "Score of current game: " + str(score), 20, 1*WIDTH / 4, 40)
        draw_text(screen, "Max score: " + str(ireader('best_score.txt')), 20, 3 * WIDTH / 4, 40)
        draw_text(screen, "Name of current player: " + ireader('cur_name.txt'), 20, 1 * WIDTH / 4, 10)
        if ireader('best_player_name.txt') == '':
            draw_text(screen, "Name of best player: " + 'You will be the first!', 20, 3 * WIDTH / 4, 10)
        else:
            draw_text(screen, "Name of best player: " + ireader('best_player_name.txt'), 20, 3 * WIDTH / 4, 10)
# flipping screen after drawing
        pygame.display.flip()
pygame.quit()