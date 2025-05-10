import pygame
from pygame.mixer import find_channel

WIDTH = 1920
HEIGHT = 1080
FPS = 30

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("subsurf")
clock = pygame.time.Clock()

img_surf = pygame.image.load("background.jfif").convert_alpha()
img_surf = pygame.transform.scale(img_surf, (WIDTH, HEIGHT))
img_hero = pygame.image.load("./hero.png").convert_alpha()
img_hero2 = pygame.image.load("./hero2.png").convert_alpha()

walk_sound = pygame.mixer.Sound('walk_sound.mp3')
walk_channel = pygame.mixer.Channel(1)

music_files = ["music1.mp3", "music2.mp3", "music3.mp3"]
current_track = 0
pygame.mixer.music.load(music_files[current_track])
pygame.mixer.music.play()

font = pygame.font.SysFont("Arial", 48, bold=True)


class Hero(pygame.sprite.Sprite):
    def __init__(self, name, age, image, x, y):
        super().__init__()
        self.name = name
        self.age = age
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT


class Money(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=20):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


hero1 = Hero("hero", 40, img_hero, 500, 750)
hero2 = Hero("hero2", 16, img_hero2, 750, 750)

all_sprites = pygame.sprite.Group()
money_group = pygame.sprite.Group()
all_sprites.add(hero1, hero2)

MONEY_Y = HEIGHT - 200

MONEY_SPACING = 180
for x in range(100, WIDTH - 100, MONEY_SPACING):
    coin = Money(x, MONEY_Y)
    money_group.add(coin)
    all_sprites.add(coin)

score = 0
win_sound_played = False

running = True
while running:
    if not pygame.mixer.music.get_busy():
        current_track = (current_track + 1) % len(music_files)
        pygame.mixer.music.load(music_files[current_track])
        pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero1.x_change = -5
            if event.key == pygame.K_RIGHT:
                hero1.x_change = 5
            if event.key == pygame.K_UP:
                hero1.y_change = -5
            if event.key == pygame.K_DOWN:
                hero1.y_change = 5

            if event.key == pygame.K_a:
                hero2.x_change = -10
            if event.key == pygame.K_d:
                hero2.x_change = 10
            if event.key == pygame.K_w:
                hero2.y_change = -10
            if event.key == pygame.K_s:
                hero2.y_change = 10

            if not walk_channel.get_busy() and (
                    hero1.x_change != 0 or hero1.y_change != 0 or hero2.x_change != 0 or hero2.y_change != 0):
                walk_channel.play(walk_sound, loops=-1)

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                hero1.x_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                hero1.y_change = 0

            if event.key in (pygame.K_a, pygame.K_d):
                hero2.x_change = 0
            if event.key in (pygame.K_w, pygame.K_s):
                hero2.y_change = 0

            if hero1.x_change == 0 and hero1.y_change == 0 and hero2.x_change == 0 and hero2.y_change == 0:
                walk_channel.stop()

    for hero in [hero1, hero2]:
        coins_collected = pygame.sprite.spritecollide(hero, money_group, True)
        if coins_collected:
            pygame.mixer.Sound('monetka.mp3').play()
            score += len(coins_collected)

    screen.blit(img_surf, (0, 0))
    all_sprites.update()
    all_sprites.draw(screen)

    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    bg_rect = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10), pygame.SRCALPHA)
    bg_rect.fill((0, 0, 0, 180))
    screen.blit(bg_rect, (20, 20))
    screen.blit(score_text, (400, 100))

    if score >= 10 and not win_sound_played:
        text = font.render("Вы победили! Ваш счет равен десяти", True, (255, 255, 255))
        screen.blit(text, (960 - text.get_width() // 2, 540 - text.get_height() // 2))
        pygame.mixer.Sound('win.mp3').play()
        win_sound_played = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()