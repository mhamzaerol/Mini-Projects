'''
	Type 0:
		##.
		.##
		...
	Type 1:
		.##
		##.
		...
	Type 2:
		####
		....
		....
		....
	Type 3:
		###
		..#
		...
	Type 4:
		###
		#..
		...
	Type 5:
		.#.
		###
		...
	Type 6:
		##
		##
'''

import pygame
from config import *
from grid import get_x, get_y
from math import floor

objects = []
objects.append([[1, 1, 0], [0, 1, 1], [0, 0, 0]]) #Type 0
objects.append([[0, 1, 1], [1, 1, 0], [0, 0, 0]]) #Type 1
objects.append([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]) #Type 2
objects.append([[1, 0, 0], [1, 1, 1], [0, 0, 0]]) #Type 3
objects.append([[0, 0, 1], [1, 1, 1], [0, 0, 0]]) #Type 4
objects.append([[0, 1, 0], [1, 1, 1], [0, 0, 0]]) #Type 5
objects.append([[1, 1], [1, 1]]) #Type 6

colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (192,192,192)]

class Object:

	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.color = colors[type]
		self.object = objects[type][:]

	def inbounds(self, object):
		sz = len(object)

		for i in range(sz):
			for j in range(sz):
				if object[i][j] == 1:
					if self.x + j < 0:
						return False		
					if floor(self.x) + j >= GRID_W:
						return False
					if floor(self.y) + i >= GRID_H:
						return False
		return True

	def shift(self, new_obj, grid):
		hold_x = self.x
		hold_y = self.y
		sz = len(self.object)
		delta = []
		for i_y in range(-(sz // 2), sz // 2 + 1):
			for i_x in range(-(sz // 2), sz // 2 + 1):
				delta.append((i_x, i_y))
		
		def mag(v):
			return v[0] * v[0] + v[1] * v[1]

		delta = sorted(delta, key = mag)
		
		for v in delta:
			self.x = hold_x + v[0]
			self.y = hold_y + v[1]
			if self.inbounds(new_obj) and not grid.collide(new_obj, self.x, self.y):
				self.object = new_obj
				return

		self.x = hold_x
		self.y = hold_y

	def rotate(self, grid):
		sz = len(self.object)

		new_obj = [[0 for j in range(sz)] for i in range(sz)]
		for i in range(sz):
			for j in range(sz):
				new_obj[j][sz - i - 1] = self.object[i][j]

		self.shift(new_obj, grid)

	def display(self, window):

		sz = len(self.object)
		for i in range(sz):
			for j in range(sz):
				if self.object[i][j] == 1:
					pygame.draw.rect(window, self.color, (get_x(self.x + j), get_y(self.y + i), CELL_SIZE, CELL_SIZE))
				
	def display_sideways(self, window, x, y):
		hold_x = self.x
		hold_y = self.y
		self.x = x
		self.y = y
		self.display(window)
		self.x = hold_x
		self.y = hold_y

	def move_lr(self, vel, grid):
		self.x += vel
		if not self.inbounds(self.object) or grid.collide(self.object, self.x, self.y):
			self.x -= vel
			return False
		return True

	def move_down(self, vel, grid):
		self.y += vel
		if not self.inbounds(self.object) or grid.collide(self.object, self.x, self.y):
			self.y -= vel
			return False
		return True


