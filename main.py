import pygame
from pygame.mixer import find_channel

WIDTH = 1920
HEIGHT = 1080
FPS = 30

# создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("subsurf")
clock = pygame.time.Clock()

# Загрузка изображений
img_surf = pygame.image.load("background.jfif").convert_alpha()
img_surf = pygame.transform.scale(img_surf, (WIDTH, HEIGHT))
img_hero = pygame.image.load("./hero.png").convert_alpha()
img_hero2 = pygame.image.load("./hero2.png").convert_alpha()

walk = ('walk_sound.mp3')

music_files = ["music1.mp3", "music2.mp3", "music3.mp3"]
current_track = 0
pygame.mixer.music.load(music_files[current_track])
pygame.mixer.music.play()

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

hero1 = Hero("hero", 40, img_hero, 500, 750)
hero2 = Hero("hero2", 16, img_hero2, 750, 750)

all_sprites = pygame.sprite.Group()
all_sprites.add(hero1, hero2)

running = True
while running:
    # Проверка, закончилась ли музыка
    if not pygame.mixer.music.get_busy():  # если не играет
        current_track = (current_track + 1) % len(music_files)  # следующий трек
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

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                hero1.x_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                hero1.y_change = 0

            if event.key in (pygame.K_a, pygame.K_d):
                hero2.x_change = 0
            if event.key in (pygame.K_w, pygame.K_s):
                hero2.y_change = 0

    screen.blit(img_surf, (0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
