import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (20, 20, 50)  # Dark purple

# Colors
PLAYER_COLOR = (0, 255, 255)  # Neon cyan
ENEMY_COLOR = (255, 140, 0)  # Bright orange
TEXT_COLOR = (255, 255, 255)  # White
FLASHING_RED = [(255, 0, 0), (200, 0, 0), (150, 0, 0)]

# Player settings
PLAYER_SIZE = 50
PLAYER_POS = [WIDTH // 2, HEIGHT - (2 * PLAYER_SIZE)]

# Enemy settings
ENEMY_SIZE = 50
ENEMY_LIST = []
SPEED = 10

# Game variables
score = 0
high_score = 0
game_over = False

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("monospace", 35)
endFont = pygame.font.SysFont("comicsansms", 40, True, False)

def reset_game():
    global PLAYER_POS, ENEMY_LIST, score, SPEED, game_over
    PLAYER_POS = [WIDTH // 2, HEIGHT - (2 * PLAYER_SIZE)]
    ENEMY_LIST.clear()
    score = 0
    SPEED = 10
    game_over = False

def set_level(score):
    if score < 20:
        return 10
    elif score < 40:
        return 12
    elif score < 60:
        return 15
    else:
        return 20

def drop_enemies():
    if len(ENEMY_LIST) < 10 and random.random() < 0.1:
        x_pos = random.randint(0, WIDTH - ENEMY_SIZE)
        ENEMY_LIST.append([x_pos, 0])

def update_enemy_positions():
    global score
    for enemy in ENEMY_LIST[:]:
        if enemy[1] >= 0 and enemy[1] < HEIGHT:
            enemy[1] += SPEED
        else:
            ENEMY_LIST.remove(enemy)
            score += 1

def detect_collision(player, enemy):
    p_x, p_y = player
    e_x, e_y = enemy
    if (e_x >= p_x and e_x < (p_x + PLAYER_SIZE)) or (p_x >= e_x and p_x < (e_x + ENEMY_SIZE)):
        if (e_y >= p_y and e_y < (p_y + PLAYER_SIZE)) or (p_y >= e_y and p_y < (e_y + ENEMY_SIZE)):
            return True
    return False

def collision_check():
    for enemy in ENEMY_LIST:
        if detect_collision(PLAYER_POS, enemy):
            return True
    return False

def limit():
    PLAYER_POS[0] = max(0, min(WIDTH - PLAYER_SIZE, PLAYER_POS[0]))
    PLAYER_POS[1] = max(0, min(HEIGHT - PLAYER_SIZE, PLAYER_POS[1]))

# Game loop
flash_index = 0
while True:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PLAYER_POS[0] -= PLAYER_SIZE
            elif event.key == pygame.K_RIGHT:
                PLAYER_POS[0] += PLAYER_SIZE
            elif event.key == pygame.K_UP:
                PLAYER_POS[1] -= PLAYER_SIZE
            elif event.key == pygame.K_DOWN:
                PLAYER_POS[1] += PLAYER_SIZE
            elif event.key == pygame.K_SPACE and game_over:
                reset_game()

    limit()

    if not game_over:
        drop_enemies()
        update_enemy_positions()
        SPEED = set_level(score)
        if collision_check():
            game_over = True
            high_score = max(high_score, score)

    for enemy in ENEMY_LIST:
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE), border_radius=10)

    pygame.draw.rect(screen, PLAYER_COLOR, (PLAYER_POS[0], PLAYER_POS[1], PLAYER_SIZE, PLAYER_SIZE), border_radius=10)

    score_label = myFont.render(f"Score: {score}", 1, TEXT_COLOR)
    high_score_label = myFont.render(f"High Score: {high_score}", 1, TEXT_COLOR)
    screen.blit(score_label, (WIDTH - 200, HEIGHT - 50))
    screen.blit(high_score_label, (20, HEIGHT - 50))

    if game_over:
        flash_index = (flash_index + 1) % len(FLASHING_RED)
        final_score_label = endFont.render(f"Final Score: {score}", 1, FLASHING_RED[flash_index])
        restart_label = endFont.render("Press SPACE to Restart", 1, TEXT_COLOR)
        screen.blit(final_score_label, (250, 250))
        screen.blit(restart_label, (200, 300))

    pygame.display.update()
    clock.tick(30)
