import pygame
import random
import sys

# Simple Snake Game using pygame

pygame.init()

WIDTH, HEIGHT = 640, 480
CELL = 20
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_text(text, pos, color=(255,255,255)):
	img = font.render(text, True, color)
	screen.blit(img, pos)

def random_cell():
	x = random.randint(0, (WIDTH//CELL)-1) * CELL
	y = random.randint(0, (HEIGHT//CELL)-1) * CELL
	return x, y

def main():
	snake = [(CELL*5, CELL*5), (CELL*4, CELL*5), (CELL*3, CELL*5)]
	direction = (1, 0)  # moving right
	food = random_cell()
	score = 0
	running = True

	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				elif event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
					direction = (0, -1)
				elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
					direction = (0, 1)
				elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
					direction = (-1, 0)
				elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
					direction = (1, 0)

		# move snake
		head_x, head_y = snake[0]
		dx, dy = direction
		new_head = (head_x + dx*CELL, head_y + dy*CELL)

		# check collisions with walls
		if (new_head[0] < 0 or new_head[0] >= WIDTH or
			new_head[1] < 0 or new_head[1] >= HEIGHT or
			new_head in snake):
			# game over
			draw_game_over(screen, score)
			pygame.display.flip()
			pygame.time.wait(1500)
			return

		snake.insert(0, new_head)

		# check food
		if new_head == food:
			score += 1
			food = random_cell()
		else:
			snake.pop()

		# draw
		screen.fill((0, 0, 0))
		for seg in snake:
			pygame.draw.rect(screen, (0,255,0), (*seg, CELL, CELL))
		pygame.draw.rect(screen, (255,0,0), (*food, CELL, CELL))
		draw_text(f"Score: {score}", (10, 10))
		pygame.display.flip()

def draw_game_over(surface, score):
	surface.fill((0,0,0))
	go_font = pygame.font.SysFont(None, 72)
	img = go_font.render('Game Over', True, (255, 0, 0))
	surface.blit(img, ((WIDTH - img.get_width())//2, (HEIGHT - img.get_height())//2 - 30))
	font_small = pygame.font.SysFont(None, 36)
	s = font_small.render(f'Score: {score}', True, (255,255,255))
	surface.blit(s, ((WIDTH - s.get_width())//2, (HEIGHT - s.get_height())//2 + 30))

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print('Error:', e)
	finally:
		pygame.quit()
		sys.exit()
