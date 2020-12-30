import pygame
from config import *
from sessions import Session, render_decorator
from button import Button
from datetime import datetime
from tohome import Tohome

class ScoreSave(Session):

	def __init__(self, sub_session, app):
		super().__init__(sub_session, app)
		self.save_button = Button(MID_X - 100, MID_Y - 20, 200, 40, 'Save', H_BUTTON_COLOR)
		self.nickname = ''
		self.cursor_cooldown = 0
		self.cursor_sign = 1

	def on_event(self, event):
		super().on_event(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if self.save_button.is_over(pos):
				self.done()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				self.nickname = self.nickname[:-1]
			elif event.key == pygame.K_RETURN:
				self.done()
			else:
				self.nickname += event.unicode

	def done(self):
		self.running = False
		now = datetime.now()
		self.app.scoreboard.add_score([self.nickname, now.strftime("%m/%d/%Y"), str(self.app.temp_score)])
		self.sibling_session = Tohome

	@render_decorator
	def on_render(self):	
		self.save_button.display(self.app.window)
		
		font = pygame.font.SysFont('comicsans', 40)
		cursor = ''
		if self.cursor_sign == 1:
			cursor = '|'
			self.cursor_cooldown += 1
			if self.cursor_cooldown == 45:
				self.cursor_sign = -1
		else:
			self.cursor_cooldown -= 1
			if self.cursor_cooldown == 0:
				self.cursor_sign = 1
		text = font.render(f'Nickname: {self.nickname}{cursor}', 1, WHITE)
		self.app.window.blit(text, (50, 200))

