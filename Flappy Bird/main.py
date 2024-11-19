import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# Load assets from 'sprites' folder in the same directory as the script
ASSET_PATH = os.path.join(os.path.dirname(__file__), 'sprites')
bg = pygame.image.load(os.path.join(ASSET_PATH, "background-day.png"))
base = pygame.image.load(os.path.join(ASSET_PATH, "base.png"))
bird_frames = [
    pygame.image.load(os.path.join(ASSET_PATH, "yellowbird-downflap.png")),
    pygame.image.load(os.path.join(ASSET_PATH, "yellowbird-midflap.png")),
    pygame.image.load(os.path.join(ASSET_PATH, "yellowbird-upflap.png")),
]
pipe_surface = pygame.image.load(os.path.join(ASSET_PATH, "pipe-green.png"))

# Digit sprites for scores
digit_sprites = {str(i): pygame.image.load(os.path.join(ASSET_PATH, f"{i}.png")) for i in range(10)}

# Game variables
gravity = 0.25
bird_movement = 0
bird_index = 0
bird_rect = bird_frames[bird_index].get_rect(center=(50, SCREEN_HEIGHT // 2))

base_x = 0
pipe_gap = 150
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

score = 0
high_score = 0
game_active = True

# Functions
def draw_base():
    screen.blit(base, (base_x, SCREEN_HEIGHT - 100))
    screen.blit(base, (base_x + SCREEN_WIDTH, SCREEN_HEIGHT - 100))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = {"rect": pipe_surface.get_rect(midtop=(SCREEN_WIDTH + 50, random_pipe_pos)), "scored": False}
    top_pipe = {"rect": pipe_surface.get_rect(midbottom=(SCREEN_WIDTH + 50, random_pipe_pos - pipe_gap)), "scored": False}
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe["rect"].centerx -= 5
    return [pipe for pipe in pipes if pipe["rect"].right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe["rect"].bottom >= SCREEN_HEIGHT:  # Bottom pipe
            screen.blit(pipe_surface, pipe["rect"])
        else:  # Top pipe (flipped)
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe["rect"])

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe["rect"]):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT - 100:
        return False
    return True

def display_score(score, x, y):
    score_str = str(score)
    for idx, digit in enumerate(score_str):
        screen.blit(digit_sprites[digit], (x + idx * 20, y))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -7
            if event.key == pygame.K_SPACE and not game_active:
                # Reset game
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, SCREEN_HEIGHT // 2)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Background
    screen.blit(bg, (0, 0))

    if game_active:
        # Bird animation
        bird_movement += gravity
        bird_rect.centery += bird_movement

        bird_index = (bird_index + 1) % 3
        screen.blit(bird_frames[bird_index], bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)

        # Scoring logic
        for pipe in pipe_list:
            if pipe["rect"].centerx < bird_rect.centerx and not pipe["scored"]:
                score += 1
                pipe["scored"] = True  # Mark pipe as scored

        display_score(score, SCREEN_WIDTH // 2 - 20, 50)
    else:
        # Game over
        high_score = max(score, high_score)
        display_score(high_score, SCREEN_WIDTH // 2 - 20, 50)

    # Base
    base_x -= 1
    if base_x <= -SCREEN_WIDTH:
        base_x = 0
    draw_base()

    pygame.display.update()
    clock.tick(FPS)
