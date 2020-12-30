import pygame
from config import *
from sessions import Session
from home import Home
from scoreboard import Scoreboard
from tohome import Tohome

class App(Session):

	def __init__(self, sub_session):
		self.init_window()
		super().__init__(sub_session, None)
		self.scoreboard = Scoreboard('high_scores.txt', MAXSCORES)
		self.clock = pygame.time.Clock()
		self.temp_score = None

	def init_window(self):
		pygame.font.init()
		self.window = pygame.display.set_mode(SIZE)
		pygame.display.set_caption("Tetris Game")
		
	def cleanup(self):
		self.scoreboard.save()
		pygame.quit()

	def update_running(self):
		if self.sub_session == None:
			self.running = False

	def on_execute(self):
		self.update_running()
		while self.running:
			sub_session = self.sub_session(None, self)
			self.sub_session = sub_session.on_execute()
			if self.sub_session == Tohome:
				self.sub_session = Home
			self.update_running()
		self.cleanup()

if __name__ == '__main__':
	the_app = App(Home)
	the_app.on_execute()
