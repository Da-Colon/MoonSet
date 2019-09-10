'''
=========
BUG SPRAY
=========
[x] Fix Player 1 y-axis limitiations - RR
[] Fix Player 2 y-axis limititions - RR
[] Decrease progress count - RR

=============
STRETCH GOALS
=============
[] Player health bar color changes as health decreases - RR
'''
import pygame
import random
from os import path


img_dir = path.join(path.dirname(__file__), 'img')
# File path with all the enemy images
enemy_ship_dir = path.join(img_dir, 'SpaceShooterRedux/PNG/Enemies')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MoonSet")
clock = pygame.time.Clock()

# Renders text on screen
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    a = Mob()
    all_sprites.add(a)
    mob.add(a)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH 
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    if fill < 30:
        pygame.draw.rect(surf, RED, fill_rect)

def progress_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH 
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, YELLOW, outline_rect, 4)
# ? The Menu and the Game Over Screen are the same. For now.


def show_gameover_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "MoonSet!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow Keys move, Space to fire",
              22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press C to Continue", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    waiting = False

# Creates sprites for player, mobs, and bullets
#! PLAYER 1 SETTINGS
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        # self.image.fill(GREEN)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        # pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH * .25
        self.rect.bottom = HEIGHT - 15
        self.speedx = 0
        self.speedy = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

#! PLAYER 2 SETTINGS
class Player2Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        # self.image.fill(GREEN)
        self.image = pygame.transform.scale(player2_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        # pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH * .75
        self.rect.bottom = HEIGHT - 15
        self.speedx = 0
        self.speedy = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_w]:
            self.speedy = -5
        if keystate[pygame.K_s]:
            self.speedy = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

#! MOB SETTINGS / ENEMY SETTINGS
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemy_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 4)
        self.speedx = random.randrange(-1, 1)
        # Commenting out rotation related attributes and methods as enemy ships don't need them
        # self.rot = 0
        # self.rot_speed = random.randrange(-8, 8)
        # self.last_update = pygame.time.get_ticks()

    # def rotate(self):
    #     now = pygame.time.get_ticks()
    #     if now - self.last_update > 50:
    #         self.last_update = now
    #         self.rot = (self.rot + self.rot_speed) % 360
    #         new_image = pygame.transform.rotate(self.image_orig, self.rot)
    #         old_center = self.rect.center
    #         self.image = new_image
    #         self.rect = self.image.get_rect()
    #         self.rect.center = old_center


    def update(self):
        # self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 4)
    
    def shoot(self):
        enemy_bullet = Enemy_Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)
        # shoot_sound.play()

# Bullet for the Player Ship
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Bullet for the Enemy Ship
class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "6776.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip.png")).convert()
player2_img = pygame.image.load(path.join(img_dir, "player2Ship.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
enemy_bullet_img = pygame.image.load(
    path.join(img_dir, "laserGreen02.png")).convert()
enemy_images = []
enemy_list = ['enemyBlack2.png', 'enemyBlue3.png',
              'enemyGreen4.png', 'enemyRed5.png']
for img in enemy_list:
    enemy_images.append(pygame.image.load(
        path.join(enemy_ship_dir, img)).convert())

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
expl_sound = []
for snd in ['expl1.wav', 'expl2.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'Lunar Harvest v1_0.mp3'))
pygame.mixer.music.set_volume(0.6)


# Define sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
mob = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = PlayerShip()
player2 = Player2Ship()
all_sprites.add(player)
all_sprites.add(player2)


# Spawns up to 3 Enemy Ships by added them to the all_sprites group allow them to be drawn
for i in range(3):
    newmob()

score = 0
progress = 0
game_over = True
running = True
pygame.mixer.music.play(loops=-1)



# Game loop
while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    if game_over:
        show_gameover_screen()
        game_over = False
        # When we come back from game over screen, we need to reload all the game objects
        all_sprites = pygame.sprite.Group()
        mob = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        player = PlayerShip()
        player2 = Player2Ship()
        all_sprites.add(player)
        all_sprites.add(player2)
        
        for i in range(3):
            newmob()
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()                 #TODO Add a Function alive() so that we check for player being alive
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                player2.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                for a in mob:
                    a.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # * Update
    all_sprites.update()

    # yaCollisions
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mob, bullets, True, True)
    for hit in hits:
        newmob()
        score += 50 - hit.radius
        progress += 3
        random.choice(expl_sound).play()

    #check to see if a mob hit the player1
    hits = pygame.sprite.spritecollide(player, mob, True, pygame.sprite.collide_circle)
    for hit in hits: 
        player.shield -= hit.radius * 2
        random.choice(expl_sound).play()
        newmob()
        if player.shield <= 0:
            player.kill()

    # check to see if a mob hit the player2
    hits = pygame.sprite.spritecollide(player2, mob, True, pygame.sprite.collide_circle)
    for hit in hits: 
        player2.shield -= hit.radius * 2
        newmob()
        random.choice(expl_sound).play()
        if player2.shield <= 0:
            player2.kill()

    if player.shield <= 0 and player2.shield <= 0:
        game_over = True
        
        
        # check to see if an enemy bullet hit the players
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 20
        if player.shield <= 0:
            player.kill()

    hits = pygame.sprite.spritecollide(player2, enemy_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player2.shield -= 20
        if player2.shield <= 0:
            player2.kill()

    

        
        

    


    # * Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 30)
    draw_shield_bar(screen, 5, 5, player.shield)
    progress_bar(screen, WIDTH / 2 -75, 5, progress) #! CORRECTLY LINK BOSS BATTLE
    draw_shield_bar(screen, 370, 5, player2.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
