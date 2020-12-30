import pygame
from config import *
from button import Button
from game import Game
from sessions import Session, render_decorator

class Scores(Session):

	def __init__(self, sub_session, app):
		super().__init__(sub_session, app)
		self.play_button = Button(WIDTH - 220, 20, 200, 40, 'Play', H_BUTTON_COLOR)

	def on_event(self, event):
		super().on_event(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if self.play_button.is_over(pos):
				self.running = False
				self.sibling_session = Game

	@render_decorator
	def on_render(self):
		self.play_button.display(self.app.window)
		self.app.scoreboard.display(self.app.window, self.play_button.height + 40)