import pygame
import os
from pygame.mixer import find_channel

WIDTH = 1920
HEIGHT = 1080
FPS = 165
TILE_SIZE = 50
GROUND_LEVEL_OFFSET = 100
HERO_SPEED_X = 5

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("subsurf")
clock = pygame.time.Clock()

img_surf = pygame.image.load("photos/background.jfif").convert_alpha()
img_surf = pygame.transform.scale(img_surf, (WIDTH, HEIGHT))
img_hero = pygame.image.load("photos/hero.png").convert_alpha()
img_hero2 = pygame.image.load("photos/hero2.png").convert_alpha()

walk_sound = pygame.mixer.Sound('sounds/walk_sound.mp3')
walk_channel = pygame.mixer.Channel(1)

music_files = ["sounds/music1.mp3", "sounds/music2.mp3", "sounds/music3.mp3"]
current_track = 0
pygame.mixer.music.load(music_files[current_track])
pygame.mixer.music.play()

font = pygame.font.SysFont("Arial", 48, bold=True)

BLOCK_NAMES = [
    "wood", "planks", "glass", "sand", "dirt",
    "stone", "gravel", "leaves", "obsidian", "coal"
]
BLOCK_TYPES = []

for name in BLOCK_NAMES:
    path = os.path.join("blocks", f"{name}.jpg")
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    BLOCK_TYPES.append({"name": name.capitalize(), "image": image})

selected_block_index = 0
placed_blocks = []

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super().__init__()
        self.image = BLOCK_TYPES[block_type]["image"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -12
        self.on_ground = False

    def update(self):
        self.rect.x += self.x_change
        if pygame.sprite.spritecollide(self, placed_blocks_group, False):
            if self.x_change > 0:
                self.rect.right = min([block.rect.left for block in placed_blocks_group if block.rect.colliderect(self.rect)])
            elif self.x_change < 0:
                self.rect.left = max([block.rect.right for block in placed_blocks_group if block.rect.colliderect(self.rect)])

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if pygame.sprite.spritecollide(self, placed_blocks_group, False):
            if self.velocity_y > 0:
                self.rect.bottom = min([block.rect.top for block in placed_blocks_group if block.rect.colliderect(self.rect)])
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y < 0:
                self.rect.top = max([block.rect.bottom for block in placed_blocks_group if block.rect.colliderect(self.rect)])
                self.velocity_y = 0

        if self.rect.bottom >= HEIGHT - GROUND_LEVEL_OFFSET:
            self.rect.bottom = HEIGHT - GROUND_LEVEL_OFFSET
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_strength

class Money(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=20):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def draw_inventory(surface):
    for i, block in enumerate(BLOCK_TYPES):
        rect = pygame.Rect(10 + i * 60, HEIGHT - 60, 50, 50)
        surface.blit(block["image"], rect.topleft)
        if i == selected_block_index:
            pygame.draw.rect(surface, (255, 255, 0), rect, 3)
        else:
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)

def draw_blocks(surface):
    for block in placed_blocks_group:
        surface.blit(block.image, block.rect.topleft)

hero1 = Hero("hero", 40, img_hero, 500, 750)
hero2 = Hero("hero2", 16, img_hero2, 750, 750)

all_sprites = pygame.sprite.Group()
money_group = pygame.sprite.Group()
all_sprites.add(hero1, hero2)

placed_blocks_group = pygame.sprite.Group()

MONEY_Y = HEIGHT - 200 - GROUND_LEVEL_OFFSET
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
                hero1.x_change = -HERO_SPEED_X
            if event.key == pygame.K_RIGHT:
                hero1.x_change = HERO_SPEED_X
            if event.key == pygame.K_UP:
                hero1.jump()

            if event.key == pygame.K_a:
                hero2.x_change = -HERO_SPEED_X
            if event.key == pygame.K_d:
                hero2.x_change = HERO_SPEED_X
            if event.key == pygame.K_w:
                hero2.jump()

            if pygame.K_1 <= event.key <= pygame.K_9:
                selected_block_index = event.key - pygame.K_1
            elif event.key == pygame.K_0:
                selected_block_index = 9

            if not walk_channel.get_busy() and (
                    hero1.x_change != 0 or hero1.velocity_y != 0 or hero2.x_change != 0 or hero2.velocity_y != 0):
                walk_channel.play(walk_sound, loops=-1)

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                hero1.x_change = 0

            if event.key in (pygame.K_a, pygame.K_d):
                hero2.x_change = 0

            if hero1.x_change == 0 and hero1.velocity_y == 0 and hero2.x_change == 0 and hero2.velocity_y == 0:
                walk_channel.stop()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = (mouse_x // TILE_SIZE) * TILE_SIZE
            grid_y = (mouse_y // TILE_SIZE) * TILE_SIZE
            if event.button == 3:
                placed_blocks.append(((grid_x, grid_y), selected_block_index))
                block = Block(grid_x, grid_y, selected_block_index)
                placed_blocks_group.add(block)
            elif event.button == 1:
                for block in placed_blocks_group:
                    if block.rect.collidepoint(mouse_x, mouse_y):
                        placed_blocks_group.remove(block)

    for hero in [hero1, hero2]:
        coins_collected = pygame.sprite.spritecollide(hero, money_group, True)
        if coins_collected:
            pygame.mixer.Sound('sounds/monetka.mp3').play()
            score += len(coins_collected)

    screen.blit(img_surf, (0, 0))
    draw_blocks(screen)
    all_sprites.update()
    all_sprites.draw(screen)

    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    bg_rect = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10), pygame.SRCALPHA)
    bg_rect.fill((0, 0, 0, 180))
    screen.blit(bg_rect, (20, 20))
    screen.blit(score_text, (400, 100))

    draw_inventory(screen)

    if score >= 10 and not win_sound_played:
        text = font.render("Вы победили! Ваш счет равен десяти", True, (255, 255, 255))
        screen.blit(text, (960 - text.get_width() // 2, 540 - text.get_height() // 2))
        pygame.mixer.Sound('sounds/win.mp3').play()
        win_sound_played = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
