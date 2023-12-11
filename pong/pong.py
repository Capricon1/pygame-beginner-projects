import pygame, sys, time, random

WIDTH = 1280
HEIGHT = 720

class Game:

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Pong')

		# players
		self.player_left = pygame.Rect(10, HEIGHT / 2 - 60, 6, 120)
		self.player_left_posy = self.player_left.y
		self.player_right = pygame.Rect(WIDTH - (10 + 6), HEIGHT / 2 - 60, 6, 120)
		self.player_right_posy = self.player_right.y

		self.player_speed = 400
		self.player_left_direction = 0  # y movement
		self.player_right_direction = 0  # y movement

		# ball
		self.reset_ball()

		# setup
		self.scores = [0, 0]
		self.game_over = False
		self.timer_activate = False

		# font
		self.font = pygame.font.Font('PublicPixel.ttf', 40)
		self.big_font = pygame.font.Font('PublicPixel.ttf', 60)

		# import sounds
		self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
		self.hit_sound.set_volume(0.5)
		self.collide_sound = pygame.mixer.Sound('sounds/collide.wav')
		self.collide_sound.set_volume(0.2)

	def reset_ball(self):
		self.ball = pygame.Rect(WIDTH / 2 - 5, random.randint(0, HEIGHT), 10, 10)
		self.ball_pos = pygame.math.Vector2(self.ball.topleft)
		self.ball_direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
		self.ball_speed = 280

		self.start_time = pygame.time.get_ticks()

	def keyboard_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_e] and self.player_left.top > 0: self.player_left_direction = -1
		elif keys[pygame.K_d] and self.player_left.bottom < HEIGHT: self.player_left_direction = 1
		else: self.player_left_direction = 0
		if keys[pygame.K_i] and self.player_right.top > 0: self.player_right_direction = -1
		elif keys[pygame.K_k] and self.player_right.bottom < HEIGHT: self.player_right_direction = 1
		else: self.player_right_direction = 0

	def player_movement(self, dt):
		# player left movement
		self.player_left_posy += self.player_left_direction * self.player_speed * dt
		self.player_left.y = round(self.player_left_posy)
		# player right movement
		self.player_right_posy += self.player_right_direction * self.player_speed * dt
		self.player_right.y = round(self.player_right_posy)

	def boundary_constraint(self):
		if self.ball.top <= 0:
			self.ball.top = 1
			self.ball_direction.y = -self.ball_direction.y
			self.ball_pos.y = self.ball.y
			self.collide_sound.play()
		if self.ball.bottom >= HEIGHT:
			self.ball.bottom = HEIGHT - 1
			self.ball_direction.y = -self.ball_direction.y
			self.ball_pos.y = self.ball.y
			self.collide_sound.play()

	def ball_movement(self, dt):
		self.ball_pos += self.ball_direction * self.ball_speed * dt
		self.ball.topleft = (round(self.ball_pos.x), round(self.ball_pos.y))

	def collisions(self):
		if self.ball.colliderect(self.player_left):
			self.ball.left = self.player_left.right + 1
			self.ball_direction.x = -self.ball_direction.x
			self.ball_pos.x = self.ball.x
			self.hit_sound.play()
			if self.ball_speed <= 440: self.ball_speed += 20
		if self.ball.colliderect(self.player_right):
			self.ball.right = self.player_right.left - 1
			self.ball_direction.x = -self.ball_direction.x
			self.ball_pos.x = self.ball.x
			self.hit_sound.play()
			if self.ball_speed <= 440: self.ball_speed += 20

	def score(self):
		if self.ball.right < -100:
			self.reset_ball()
			self.scores[1] += 1
			self.timer_activate = True
		if self.ball.left > WIDTH + 100:
			self.reset_ball()
			self.scores[0] += 1
			self.timer_activate = True
		if self.scores[0] >= 3 or self.scores[1] >= 3:
			self.game_over = True

	def display_score(self):
		score_text = self.font.render(f'{self.scores[0]}    {self.scores[1]}', False, (126, 126, 126))
		score_rect = score_text.get_rect(midtop=(WIDTH / 2, 170))
		self.screen.blit(score_text, score_rect)

	def display_game_over(self):
		msg = self.big_font.render('GAME OVER', False, (126, 126, 126))
		msg_rect = msg.get_rect(center=(WIDTH / 2, HEIGHT / 2))
		border = pygame.Rect(msg_rect.x - 5, msg_rect.y - 5, msg_rect.width + 10, msg_rect.height + 10)
		pygame.draw.rect(self.screen, 'white', border, 0, 8)
		self.screen.blit(msg, msg_rect)

	def timer(self):
		if self.timer_activate and not self.game_over:
			past_time = pygame.time.get_ticks() - self.start_time
			remain_sec = 3 - past_time // 1000
			
			# display
			remain_text = self.big_font.render(f'{remain_sec}', True, (126, 126, 126))
			remain_rect = remain_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
			self.screen.blit(remain_text, remain_rect)
			# print(remain_sec)

			if past_time >= 3000:
				self.timer_activate = False

	def run(self):
		last_time = time.time()
		while True:
			dt = time.time() - last_time
			last_time = time.time()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if self.game_over:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						self.game_over = False
						self.start_time = pygame.time.get_ticks()
						self.scores = [0, 0]

			self.screen.fill((26, 26, 26))
			pygame.draw.line(self.screen, 'grey', (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

			self.timer()		
			# display
			pygame.draw.rect(self.screen, 'grey', self.player_left)
			pygame.draw.rect(self.screen, 'grey', self.player_right)
			pygame.draw.rect(self.screen, 'grey', self.ball)
			self.display_score()
			if self.game_over: self.display_game_over()

			if not self.timer_activate and not self.game_over:
				# input
				self.keyboard_input()
				self.player_movement(dt)
				self.ball_movement(dt)
				self.boundary_constraint()
				# collisions
				self.collisions()
				self.score()

			pygame.display.update()

Game().run()