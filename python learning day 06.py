exercise 01 

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game window size
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
SPEED = 12  # Snake speed (frames per second)

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling speed
clock = pygame.time.Clock()

# Fonts
score_font = pygame.font.SysFont("comicsansms", 30)
game_over_font = pygame.font.SysFont("comicsansms", 50)

# Snake initial position and body
snake_pos = [[WIDTH // 2, HEIGHT // 2]]
snake_direction = "RIGHT"
score = 0

# Generate random food position
def generate_food():
    while True:
        food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        if [food_x, food_y] not in snake_pos:
            return [food_x, food_y]

food_pos = generate_food()

# Display score
def show_score():
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

# Game over screen
def game_over():
    over_surface = game_over_font.render(f"Game Over! Score: {score}", True, RED)
    over_rect = over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(over_surface, over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # Move snake
    head_x, head_y = snake_pos[0]
    if snake_direction == "UP":
        head_y -= BLOCK_SIZE
    elif snake_direction == "DOWN":
        head_y += BLOCK_SIZE
    elif snake_direction == "LEFT":
        head_x -= BLOCK_SIZE
    elif snake_direction == "RIGHT":
        head_x += BLOCK_SIZE

    new_head = [head_x, head_y]

    # Check collisions with walls
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    # Check collisions with itself
    if new_head in snake_pos:
        game_over()

    # Insert new head
    snake_pos.insert(0, new_head)

    # Check if snake eats food
    if new_head == food_pos:
        score += 1
        food_pos = generate_food()
    else:
        snake_pos.pop()  # Remove tail

    # Draw everything
    screen.fill(BLACK)
    for block in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    show_score()
    pygame.display.flip()

    # Control speed
    clock.tick(SPEED)
    