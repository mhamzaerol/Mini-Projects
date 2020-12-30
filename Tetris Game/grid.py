import pygame
from config import *
from math import floor
import copy

def get_y(i):
	return GAME_OFFSET_Y + (CELL_SIZE + CELL_OUT) * floor(i) + CELL_OUT

def get_x(j):
	return GAME_OFFSET_X + (CELL_SIZE + CELL_OUT) * floor(j) + CELL_OUT

ANIM_SLOW = 2

class Grid:

	def __init__(self):
		self.cells = [[BLACK for j in range(GRID_W)] for i in range(GRID_H)]
		self.animation_time = 0
		
	def add_object(self, Obj_instance):
		sz = len(Obj_instance.object)
		x = floor(Obj_instance.x)
		y = floor(Obj_instance.y)
		for i in range(sz):
			for j in range(sz):
				if Obj_instance.object[i][j] == 1:
					c_y = y + i
					c_x = x + j
					if c_y >= 0:
						if self.cells[c_y][c_x] != BLACK:
							raise Exception()
						self.cells[c_y][c_x] = Obj_instance.color
		self.clean_lines()

	def animate_cleaning(self, window):
		for i in self.lines:
			for j in range(0, GRID_W - (self.animation_time + ANIM_SLOW - 1) // ANIM_SLOW + 1):
				pygame.draw.rect(window, BLACK, (get_x(j), get_y(i), CELL_SIZE, CELL_SIZE))
		self.animation_time -= 1
		if self.animation_time == 0:
			self.cells = self.clean_cells

	def clean_lines(self):
		self.lines = []
		self.clean_cells = copy.deepcopy(self.cells)
		cnt = 0
		for i in range(GRID_H - 1, -1, -1):
			flag = True
			for j in range(GRID_W - 1, -1, -1):
				if self.clean_cells[i][j] == BLACK:
					flag = False
					break
			if flag == True:
				cnt += 1
				self.lines.append(i)
			else:
				for j in range(GRID_W):
					self.clean_cells[i + cnt][j] = self.clean_cells[i][j]
			if cnt > 0:
				for j in range(GRID_W):
					self.clean_cells[i][j] = BLACK
		if cnt > 0:
			self.animation_time = GRID_W * ANIM_SLOW
		else:
			self.cells = self.clean_cells

	def collide(self, object, x, y):
		sz = len(object)
		x = floor(x)
		y = floor(y) 
		for i in range(sz):
			for j in range(sz):
				if object[i][j] == 1:
					c_y = y + i
					c_x = x + j
					if c_y >= 0 and c_x >= 0:
						if self.cells[c_y][c_x] != BLACK:
							return True
		return False

	def projection(self, window, Obj_instance):
		object = Obj_instance.object
		sz = len(object)
		x = floor(Obj_instance.x)
		y = floor(Obj_instance.y)
		mn_d = GRID_H
		for j in range(sz):
			for i in range(sz - 1, -1, -1):
				if object[i][j] == 1:
					c_y = y + i
					c_x = x + j
					d = 0
					while c_y < GRID_H:
						if c_y >= 0 and self.cells[c_y][c_x] != BLACK:
							break 
						c_y += 1
						d += 1
					mn_d = min(mn_d, d)
					break
		for i in range(sz):
			for j in range(sz):
				if object[i][j] == 1:
					c_y = y + i + mn_d - 1
					c_x = x + j
					pygame.draw.rect(window, Obj_instance.color, (get_x(c_x) - CELL_OUT, get_y(c_y) - CELL_OUT, CELL_SIZE + 2 * CELL_OUT, CELL_SIZE + 2 * CELL_OUT), 1)


	def display(self, window):

		for i in range(GRID_H):
			for j in range(GRID_W):
				if self.cells[i][j] != BLACK:
					pygame.draw.rect(window, self.cells[i][j], (get_x(j), get_y(i), CELL_SIZE, CELL_SIZE))
		
		for j in range(GRID_W + 1):
			pygame.draw.line(window, H_BUTTON_COLOR, (get_x(j) - CELL_OUT, get_y(0) - CELL_OUT), (get_x(j) - CELL_OUT, get_y(GRID_H) - CELL_OUT))

		for i in range(GRID_H + 1):
			pygame.draw.line(window, H_BUTTON_COLOR, (get_x(0) - CELL_OUT, get_y(i) - CELL_OUT), (get_x(GRID_W) - CELL_OUT, get_y(i) - CELL_OUT))
