import pygame
from config import *

class Button():
	def __init__(self, x, y, width, height, text, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.color = color

	def display(self, window):
		self.rect = pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), border_radius = self.height // 2)
		font = pygame.font.SysFont('comicsans', self.height)
		text = font.render(self.text, 1, WHITE)
		window.blit(text, (self.x + (self.width - text.get_width()) / 2, self.y + (self.height - text.get_height()) / 2))

	def is_over(self, pos):
		return self.rect.collidepoint(pos)
