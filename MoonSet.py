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

# Custom enemy auto fire event
ENEMY_FIRE = pygame.USEREVENT
pygame.time.set_timer(ENEMY_FIRE, 1000)
BOSS_FIRE = pygame.USEREVENT
pygame.time.set_timer(BOSS_FIRE, 1000)


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

# Menu Screen


def show_menu_screen():
    screen.blit(intro_background, intro_background_rect)
    # draw_text(screen, "THIS IS THE MENU SCREEN", 64, WIDTH / 2, HEIGHT / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Any key press will start the game
            if event.type == pygame.KEYDOWN:
                waiting = False

# Win Screen


def show_congratulations_screen():
    end_game()   
    screen.blit(congratulations_image, congratulations_image_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # Press C to start the game
                if event.key == pygame.K_c:
                    waiting = False

# Lose Screen


def show_gameover_screen():
    screen.blit(game_over_image, game_over_image_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # Space bar to start the game
                if event.key == pygame.K_SPACE:
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
        if keystate[pygame.K_a]:
            self.speedx = -7
        if keystate[pygame.K_d]:
            self.speedx = 7
        if keystate[pygame.K_w]:
            self.speedy = -7
        if keystate[pygame.K_s]:
            self.speedy = 7
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
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7
        if keystate[pygame.K_UP]:
            self.speedy = -7
        if keystate[pygame.K_DOWN]:
            self.speedy = 7
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
        # enemy ships are slightly larger than player ship
        self.image_orig = pygame.transform.scale(
            random.choice(enemy_images), (60, 48))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 4)
        self.speedx = random.randrange(-1, 1)

    def update(self):
        # self.rotate()g
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


class Rita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 100))
        self.image = pygame.transform.scale(boss_moon, (100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40
        # pygame.draw.circle(self.image,RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.y = -10
        self.speedy = 0
        self.speedx = 0
        self.shield = 100

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y <= 150:
            self.speedy = 1
        else:
            self.speedy = 0
            if self.speedx == 0:
                self.speedx = 1

            if self.rect.right == WIDTH:
                self.speedx = -1
            if self.rect.left == 0:
                self.speedx = 1

    def shoot(self):
        enemy_bullet = [Enemy_Bullet(self.rect.centerx, self.rect.top), Bullet_dia_right(
            self.rect.centerx, self.rect.top), Bullet_dia_left(self.rect.centerx, self.rect.top)]
        for b in enemy_bullet:
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

# Bullet for the Enemy Ship


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # moves the bullets to the front of the enemy ship
        self.rect.bottom = y + 100
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()


class Bullet_dia_left(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # moves the bullets to the front of the enemy ship
        self.rect.bottom = y + 100
        self.rect.centerx = x
        self.speedy = 10
        self.speedx = -5

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()


class Bullet_dia_right(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # moves the bullets to the front of the enemy ship
        self.rect.bottom = y + 100
        self.rect.centerx = x
        self.speedy = 10
        self.speedx = 5

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

#! EXPLOSIONS CLASS


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosions[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosions[self.size][self.frame]
                self.rect.center = center


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "6776.jpg")).convert()
background_rect = background.get_rect()
intro_background = pygame.image.load(
    path.join(img_dir, 'Intro.png')).convert()
intro_background_rect = intro_background.get_rect()
congratulations_image = pygame.image.load(
    path.join(img_dir, "congratulations.png"))
congratulations_image_rect = congratulations_image.get_rect()
game_over_image = pygame.image.load(path.join(img_dir, "game_over.png"))
game_over_image_rect = game_over_image.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip.png")).convert()
player2_img = pygame.image.load(
    path.join(img_dir, "player2Ship.png")).convert()
boss_moon = pygame.image.load(path.join(img_dir, "moon.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
enemy_bullet_img = pygame.image.load(
    path.join(img_dir, "laserGreen02.png")).convert()
enemy_images = []
enemy_list = ['enemyBlack2.png', 'enemyBlue3.png',
              'enemyGreen4.png', 'enemyRed5.png']
for img in enemy_list:
    enemy_images.append(pygame.image.load(
        path.join(enemy_ship_dir, img)).convert())

#! EXPLOSIONS IMAGE LOAD
explosions = {}
explosions['lg'] = []
explosions['sm'] = []
explosions['xl'] = []
explosions['xxl'] = []

for i in range (8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_xl = pygame.transform.scale(img, (100, 100)) #EXPLOSION XL
    explosions['xl'].append(img_xl)
    img_xxl = pygame.transform.scale(img, (1000, 1000)) #EXPLOSION XXL
    explosions['xxl'].append(img_xxl)
    img_lg = pygame.transform.scale(img, (75, 75)) #EXPLOSION LG
    explosions['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32)) #EXPLOSION
    explosions['sm'].append(img_sm)

# Load all game sounds 
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
expl_sound = []
for snd in ['expl1.wav', 'expl2.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
def main_music():
    pygame.mixer.music.stop() 
    pygame.mixer.music.load(path.join(snd_dir, 'Lunar Harvest v1_0.mp3'))
    pygame.mixer.music.play() 
def boss_battle():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(path.join(snd_dir, 'powerrangers.mp3'))
    pygame.mixer.music.play()
def end_game():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(path.join(snd_dir, 'fanfare.mp3'))
    pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.6)





# Define sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
mob = pygame.sprite.Group()
rita = Rita()
rita_group = pygame.sprite.Group(rita)
player = PlayerShip()
player2 = Player2Ship()
all_sprites.add(player)
all_sprites.add(player2)


# Spawns up to 4 Enemy Ships by added them to the all_sprites group allow them to be drawn
for i in range(4):
    newmob()


score = 0
progress = 0
# Menu controls the Introduction screen
menu = True
# Congratulations controls the player win screen display
congratulations = False
# game_over is the screen that displays if the player loses
game_over = False
boss = False
end_music = False
music_on = False
running = True
main_music()
count = 0
while running:

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    if menu:
        show_menu_screen()
        all_sprites = pygame.sprite.Group()
        mob = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        player = PlayerShip()
        player2 = Player2Ship()
        all_sprites.add(player)
        all_sprites.add(player2)
        for i in range(4):
            newmob()
        menu = False
        congratulations = False
    if game_over:
        show_gameover_screen()
        game_over = False
        rita.shield = 100
        progress = 0
        score = 0
        # When we come back from game over screen, we need to reload all the game objects
        all_sprites = pygame.sprite.Group()
        mob = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        player = PlayerShip()
        player2 = Player2Ship()
        all_sprites.add(player)
        all_sprites.add(player2)
        for i in range(4):
            newmob()

    if congratulations:
        show_congratulations_screen()
        congratulations = False
        menu = True
        rita.shield = 100
        progress = 0
        score = 0
        all_sprites = pygame.sprite.Group()
        mob = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        player = PlayerShip()
        player2 = Player2Ship()
        all_sprites.add(player)
        all_sprites.add(player2)
        for i in range(4):
            newmob()

    #BOSS SPAWN / RITA SPAWN
    if progress >= 100:
        for a in mob:
            a.kill()
        all_sprites.add(rita)
        rita_group.add(rita)
        

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                if player.shield > 0:
                    player.shoot() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player2.shield > 0:
                    player2.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                for a in mob:
                    a.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        # Loop through the Enemy_Fire event and shoot every second
        if event.type == ENEMY_FIRE:
            for a in mob:
                a.shoot()
        if progress >= 100:
            if rita.shield > 0:
                if event.type == BOSS_FIRE:
                    rita.shoot()

    # * Update 
    all_sprites.update()
    if progress >= 100: #BOSS SPAWN UPDATE / RITA SPAWN UPDATE
        rita_group.update()
        if not music_on: 
            boss_battle()
            music_on = True

    # Collisions
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mob, bullets, True, True)
    for hit in hits:
        newmob()
        score += 50 - hit.radius
        progress += 3
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center, 'lg')  # ! EXPLOSIONS HIT
        all_sprites.add(expl)

    #! BOSS HIT
    # check to see if a bullet hit a boss 
    hits = pygame.sprite.groupcollide(
        rita_group, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        rita.shield -= 5
        if rita.shield == 0:
            expl3 = Explosion(hit.rect.center, 'xxl')
            random.choice(expl_sound).play()
            all_sprites.add(expl3)
        else:
            expl2 = Explosion(hit.rect.center, 'xl')
            random.choice(expl_sound).play()
            all_sprites.add(expl2)
        
        
        
    def test_boom():
        expl2 = Explosion(hit.rect.center, 'xl')
        random.choice(expl_sound).play()
        all_sprites.add(expl2)

    # check to see if a mob hit the player1
    #! Player 1 mob hit
    hits = pygame.sprite.spritecollide(
        player, mob, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        newmob()
        if player.shield <= 0:
            player.kill()

    # check to see if a mob hit the player2
    #! Player 2 mob hit
    hits = pygame.sprite.spritecollide(
        player2, mob, True, pygame.sprite.collide_circle)
    for hit in hits:
        player2.shield -= hit.radius * 2
        newmob()
        if player2.shield <= 0:
            player2.kill()

        # check to see if boss hits the player
        #! Player 1 Boss hit
    hits = pygame.sprite.spritecollide(
        player, rita_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        if player.shield <= 0:
            player.kill()

        # check to see if a boss hit the player2
        #! Player 2 boss hit
    hits = pygame.sprite.spritecollide(
        player2, rita_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player2.shield -= hit.radius * 2
        if player2.shield <= 0:
            player2.kill() 
    
    if player.shield <= 0 and player2.shield <= 0:
        # Reset the game progress when both players die
        progress = 0
        score = 0
        main_music()
        game_over = True
 
    #! DEATH OF RITA

    if rita.shield <= 0:
        rita.kill()
        congratulations = True
        

    # check to see if an enemy bullet hit the players
    #! MOB BULLET HIT PLAYER 1
    hits = pygame.sprite.spritecollide(
        player, enemy_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10 #PLAYER 1 HEALTH
        test_boom()#! EXPLOSION 
        if player.shield <= 0:
            player.kill()

    #! MOB BULLET HIT PLAYER 2
    hits = pygame.sprite.spritecollide(
        player2, enemy_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player2.shield -= 10 #PLAYER 2 HEALTH
        test_boom() #! EXPLOSION 
        if player2.shield <= 0:
            player2.kill()

    # * Draw / render
    screen.fill(BLACK)
    screen.blit(intro_background, intro_background_rect)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 30)
    draw_shield_bar(screen, 5, 5, player.shield)
    progress_bar(screen, WIDTH / 2 - 75, 5, progress)
    draw_shield_bar(screen, 370, 5, player2.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
