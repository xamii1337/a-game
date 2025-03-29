import pygame
from pygame.mixer import find_channel

WIDTH = 1920  # ширина игрового окна
HEIGHT = 1080  # высота игрового окна
FPS = 30  # частота кадров в секунду

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("subsurf")
clock = pygame.time.Clock()

# Загрузка изображений
img_surf = pygame.image.load("background.jfif").convert_alpha()
img_surf = pygame.transform.scale(img_surf, (WIDTH, HEIGHT))
img_hero = pygame.image.load("./hero.png").convert_alpha()
img_hero2 = pygame.image.load("./hero2.png").convert_alpha()


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

# Создание экземпляров героев с правильными именами
hero1 = Hero("hero", 40, img_hero, 500, 750)
hero2 = Hero("hero2", 16, img_hero2, 750, 750)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(hero1, hero2)  # Добавляем экземпляры класса Hero

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#
    # Отображение фона и обновление экрана
    screen.blit(img_surf, (0, 0))

    # Обновление и отрисовка всех спрайтов
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type = pygame.QUIT:
            running = False


pygame.quit()
