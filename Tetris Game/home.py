import pygame
from config import *
from button import Button
from game import Game
from scores import Scores
from sessions import Session, render_decorator

class Home(Session):

	def __init__(self, sub_session, app):
		super().__init__(sub_session, app)
		self.play_button = Button(MID_X - 100, MID_Y - 20, 200, 40, 'Play', H_BUTTON_COLOR)
		self.scores_button = Button(MID_X - 100, MID_Y + 30, 200, 40, 'High Scores', H_BUTTON_COLOR)

	def on_event(self, event):
		super().on_event(event)
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if self.play_button.is_over(pos):
				self.running = False
				self.sibling_session = Game
			if self.scores_button.is_over(pos):
				self.running = False
				self.sibling_session = Scores

	@render_decorator
	def on_render(self):
		self.play_button.display(self.app.window)
		self.scores_button.display(self.app.window)