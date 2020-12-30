import pygame
from config import *

line_sep = '$#^&'

class Scoreboard:

	def __init__(self, filename, max_size):
		self.filename = filename
		self.max_size = max_size
		self.make_scoreboard()

	def make_scoreboard(self):
		with open(self.filename, 'r+') as fd:
			lines = fd.read().splitlines()

			self.metadata = lines[0].split(line_sep)
			self.entries = []
			
			for line in lines[1:]:
				entry = line.split(line_sep)
				self.entries.append(entry)
			fd.truncate(0)

	def entry_analysis(self):
		cnt_dim = len(self.metadata)
		max_lengths = [len(meta) for meta in self.metadata]
		for entry in self.entries:
			for i in range(cnt_dim):
				max_lengths[i] = max(max_lengths[i], len(entry[i]))
		sum_lengths = sum(max_lengths)
		return [max_lengths[i] / sum_lengths for i in range(cnt_dim)]

	def display(self, window, offset_y):
		
		corr_ratios = self.entry_analysis()
		corr_lens = [int((WIDTH - 100) * i) for i in corr_ratios]
		offset_x = 50
		gap = 5

		cnt_rows = len(self.entries) + 1
		cnt_cols = len(corr_lens)

		entry_height = min(35, int((HEIGHT - offset_y) / (cnt_rows) - gap))
		
		def gen_h(n):
			h_sum = 0
			for i in range(n):
				yield offset_y + h_sum
				h_sum += entry_height + gap

		def gen_w(n):
			l_sum = 0
			for i in range(n):
				yield offset_x + l_sum
				l_sum += corr_lens[i] + gap
			
		g_h = gen_h(cnt_rows)
		for entry in [self.metadata] + self.entries:
			y = next(g_h)
			g_w = gen_w(cnt_cols)
			for i in range(cnt_cols):
				x = next(g_w)
				pygame.draw.rect(window, H_BUTTON_COLOR, (x, y, corr_lens[i], entry_height), border_radius = entry_height // 2)
				font = pygame.font.SysFont('comicsans', int(entry_height / 1.5))
				text = font.render(entry[i], 1, WHITE)
				window.blit(text, (x + (corr_lens[i] - text.get_width()) / 2, y + (entry_height - text.get_height()) / 2))	

	def add_score(self, data):
		self.entries.append(data)
		
		def score(x):
			return -int(x[-1])

		self.entries = sorted(self.entries, key=score)
		if len(self.entries) > MAXSCORES:
			self.entries = self.entries[:-1]

	def save(self):
		with open(self.filename, 'w') as fd:
			fd.write(line_sep.join(self.metadata) + '\n')
			for data in self.entries:
				fd.write(line_sep.join(data) + '\n')