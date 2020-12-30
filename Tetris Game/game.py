import pygame
from config import *
from sessions import Session, render_decorator
from object import Object
from grid import Grid
from scoresave import ScoreSave
import random

class Game(Session):

	def __init__(self, sub_session, app):
		super().__init__(sub_session, app)
		self.init_object_list()
		self.cur_object = self.object_list.pop(0)
		self.grid = Grid()
		self.cnt_the_end = 0
		self.lr_cooldown = 0
		self.d_cooldown = 0
		self.level = 1
		self.score = 0
		self.bonus = 5
		self.cnt_lines = 0
		self.base_speed = 60
		self.auto_d_cooldown = 0
		self.space_cooldown = 0

	def init_object_list(self):
		self.object_list = [Object(GRID_W / 2 - 1, -1, random.randint(0, 6)) for i in range(4)]

	def on_event(self, event):
		super().on_event(event)
		if self.grid.animation_time > 0:
			return 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				self.cur_object.rotate(self.grid)
				self.cnt_the_end = max(self.cnt_the_end - 4, 0)
			if event.key == pygame.K_p:
				self.paused = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			print(pygame.mouse.get_pos())

	def on_event_paused(self, event):
		super().on_event(event)
		super().on_event_paused(event)

	def on_events(self):
		super().on_events()
		if self.grid.animation_time > 0:
			return 
		keys = pygame.key.get_pressed()
		if keys[pygame.K_d]:
			if self.lr_cooldown == 0:
				self.cur_object.move_lr(1, self.grid)
				self.lr_cooldown = 6
		if keys[pygame.K_a]:
			if self.lr_cooldown == 0:
				self.cur_object.move_lr(-1, self.grid)
				self.lr_cooldown = 6
		if keys[pygame.K_s]:
			if self.d_cooldown == 0:
				if self.cur_object.move_down(1, self.grid):
					self.score += self.level
				self.d_cooldown = 5
		if keys[pygame.K_SPACE]:
			if self.space_cooldown == 0:
				flag = False
				while self.cur_object.move_down(1, self.grid):
					self.score += self.level
					flag = True
				if flag:
					self.score += self.bonus
				self.cnt_the_end = 35
				self.auto_d_cooldown = 0
				self.space_cooldown = 30
	
	def on_loop(self):
		if self.grid.animation_time > 0 or self.paused:
			return 

		if self.lr_cooldown > 0:
			self.lr_cooldown -= 1
		if self.d_cooldown > 0:
			self.d_cooldown -= 1
		if self.space_cooldown > 0:
			self.space_cooldown -= 1
		
		if self.auto_d_cooldown == 0:
			if not self.cur_object.move_down(1, self.grid):
				self.cnt_the_end += 2
				if self.cnt_the_end >= 35:
					self.grid.add_object(self.cur_object)
					self.score += self.level * len(self.grid.lines) * 200
					self.cnt_lines += len(self.grid.lines)
					while self.level * 5 <= self.cnt_lines:
						self.level += 1
					self.cnt_the_end = 0
					self.object_list.append(Object(GRID_W / 2 - 1, 0, random.randint(0, 6)))
					self.cur_object = self.object_list[0]
					if self.grid.collide(self.cur_object.object, self.cur_object.x, self.cur_object.y):
						self.running = False
			else:
				self.auto_d_cooldown = self.base_speed - self.level * 3
		else:
			self.auto_d_cooldown -= 1

	@render_decorator
	def on_render(self):
		if self.running:
			if self.paused:
				font = pygame.font.SysFont('comicsans', 30)
				text = font.render('Paused', 1, WHITE)
				self.app.window.blit(text, (MID_X - 50, MID_Y - 50))
				return 

			self.grid.display(self.app.window)
			if self.grid.animation_time == 0:
				if len(self.object_list) > 3:
					self.object_list.pop(0)
				self.grid.projection(self.app.window, self.cur_object)
				self.cur_object.display(self.app.window)
			else:
				self.grid.animate_cleaning(self.app.window)
			
			font = pygame.font.SysFont('comicsans', 30)
			text = font.render(f'Score: {self.score}', 1, WHITE)
			self.app.window.blit(text, (40, 450))
			text = font.render(f'Level: {self.level}', 1, WHITE)
			self.app.window.blit(text, (40, 500))
			text = font.render(f'Lines: {self.cnt_lines}', 1, WHITE)
			self.app.window.blit(text, (40, 550))
			
			u_x = GRID_W + 1
			u_y = 2
			for i in range(3):
				self.object_list[i].display_sideways(self.app.window, u_x, u_y)
				u_y += 4

	def on_cleanup(self):
		self.sibling_session = ScoreSave
		self.app.temp_score = self.score