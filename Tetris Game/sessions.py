import pygame
import time
from config import *

def render_decorator(render_f):
	def wrapper(self):
		self.app.window.fill(BLACK)
		render_f(self)
		pygame.display.update()
	return wrapper
		
class Session:

	def __init__(self, sub_session, app):
		self.sub_session = sub_session
		self.app = app
		self.running = True
		self.sibling_session = None
		self.paused = False

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
			self.sibling_session = None

	def on_event_paused(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				self.paused = False

	def on_events(self):
		paused = self.paused
		for event in pygame.event.get():
			if paused:
				self.on_event_paused(event)
			else:
				self.on_event(event)

	def on_loop(self):
		pass

	def on_render(self):
		pass

	def on_cleanup(self):
		pass

	def on_execute(self):
		while self.running:
			if self.sub_session != None:
				sub_session = self.sub_session(None)
				self.sub_session = sub_session.on_execute()
			self.on_events()
			self.on_loop()
			self.on_render()
			self.app.clock.tick(FPS)
		self.on_cleanup()
		return self.sibling_session

