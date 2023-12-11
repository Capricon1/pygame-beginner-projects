import pygame, sys, random

BOX_SIZE = 28
WIDTH = BOX_SIZE * 40
HEIGHT = BOX_SIZE * 24

class Game:

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Snake')

		# import images
		self.ground = pygame.image.load('images/ground.png').convert()
		self.snake = pygame.image.load('images/snake.png').convert_alpha()
		self.apple = pygame.image.load('images/apple.png').convert_alpha()

		# import fonts
		self.font_small = pygame.font.Font('PublicPixel.ttf', 22)
		self.font = pygame.font.Font('PublicPixel.ttf', 46)

		# import sounds
		self.eat_sound = pygame.mixer.Sound('sounds/eat.wav')
		self.eat_sound.set_volume(0.5)

		# snake setup
		self.snake_respawn()

		# food setup
		self.generate_food()

		# game setup
		self.last_time = 0
		self.game_active = True
		self.score = 0

	def snake_respawn(self):
		self.snake_rects = []
		self.snake_rects.append(pygame.Rect(BOX_SIZE * 2, 0, BOX_SIZE, BOX_SIZE))
		self.snake_rects.append(pygame.Rect(BOX_SIZE, 0, BOX_SIZE, BOX_SIZE))
		self.snake_rects.append(pygame.Rect(0, 0, BOX_SIZE, BOX_SIZE))

		self.direction = pygame.math.Vector2(1, 0)
		self.movement = 'left'

	def draw_snake(self):
		for rect in self.snake_rects:
			self.screen.blit(self.snake, rect)

	def keyboard_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			self.movement = 'up'
		elif keys[pygame.K_DOWN]:
			self.movement = 'down'
		elif keys[pygame.K_RIGHT]:
			self.movement = 'right'
		elif keys[pygame.K_LEFT]:
			self.movement = 'left'

	def snake_movement(self):
		if pygame.time.get_ticks() - self.last_time >= 120:
			self.last_time = pygame.time.get_ticks()

			if self.movement == 'up' and self.direction.y != 1: 
				self.direction.x = 0
				self.direction.y = -1
			if self.movement == 'down' and self.direction.y != -1: 
				self.direction.x = 0
				self.direction.y = 1
			if self.movement == 'right' and self.direction.x != -1: 
				self.direction.x = 1
				self.direction.y = 0
			if self.movement == 'left' and self.direction.x != 1: 
				self.direction.x = -1
				self.direction.y = 0

			if self.direction.y > 0:
				x = self.snake_rects[0].x
				y = self.snake_rects[0].y + BOX_SIZE
			if self.direction.y < 0:
				x = self.snake_rects[0].x
				y = self.snake_rects[0].y - BOX_SIZE			
			if self.direction.x > 0:
				x = self.snake_rects[0].x + BOX_SIZE
				y = self.snake_rects[0].y
			if self.direction.x < 0:
				x = self.snake_rects[0].x - BOX_SIZE
				y = self.snake_rects[0].y

			self.snake_rects.pop()
			self.snake_rects.insert(0, pygame.Rect(x, y, BOX_SIZE, BOX_SIZE))

	def boundary_constraint(self):
		if self.snake_rects[0].y > HEIGHT - BOX_SIZE:
			self.snake_rects[0].y = 0
		if self.snake_rects[0].y < 0:
			self.snake_rects[0].y = HEIGHT - BOX_SIZE
		if self.snake_rects[0].x > WIDTH - BOX_SIZE:
			self.snake_rects[0].x = 0
		if self.snake_rects[0].x < 0:
			self.snake_rects[0].x = WIDTH - BOX_SIZE

	def generate_food(self):
		while True:
			x = random.randint(0, (WIDTH / BOX_SIZE) - 1) * BOX_SIZE
			y = random.randint(0, (HEIGHT / BOX_SIZE) - 1) * BOX_SIZE
			self.food_rect = self.apple.get_rect(topleft=(x, y))
			if (x, y) not in [rect.topleft for rect in self.snake_rects]:
				break

	def food_collision(self):
		if self.snake_rects[0].colliderect(self.food_rect):
			self.snake_rects.insert(0, pygame.Rect(self.food_rect.topleft, (BOX_SIZE, BOX_SIZE)))
			self.generate_food()
			self.eat_sound.play()
			self.score += 1

	def body_collision(self):
		for index, rect in enumerate(self.snake_rects):
			if index not in [0, 1]:
				if self.snake_rects[0].colliderect(rect):
					self.game_active = False

	def draw_score(self):
		text = self.font_small.render(f'{self.score}', False, 'black')
		text_rect = text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 40))
		image_rect = self.apple.get_rect(midright=text_rect.midleft)
		self.screen.blit(self.apple, image_rect)
		self.screen.blit(text, text_rect)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if not self.game_active:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						self.snake_respawn()
						self.game_active = True
						self.score = 0


			if self.game_active:
				self.keyboard_input()
				self.snake_movement()
				self.boundary_constraint()
				self.food_collision()
				self.body_collision()

			self.screen.blit(self.ground, (0, 0))	# draw ground
			self.draw_snake()
			self.screen.blit(self.apple, self.food_rect)
			self.draw_score()
			if not self.game_active:
				text = self.font.render('GAME OVER', False, '#fdcc05')
				text_rect = text.get_rect(midtop=(WIDTH / 2, HEIGHT / 2))
				border_rect = pygame.Rect(text_rect.x - 4, text_rect.y - 4, 
					text_rect.width + 8, text_rect.height + 8)
				pygame.draw.rect(self.screen, 'black', border_rect, 0, 6)
				self.screen.blit(text, text_rect)

			pygame.display.update()

Game().run()