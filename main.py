import random
from time import time, sleep
import copy
import tkinter as tk
from PIL import Image

cell_size = 20


def save_as_png(canvas, filename):
	# save postscipt image
	canvas.postscript(file=filename + '.eps')
	# use PIL to convert to PNG
	img = Image.open(filename + '.eps')
	img.save(filename + '.png', 'png')


# Функция для создания поля
def init_grid(width, height):
	return [[random.randint(0, 1) for _ in range(width)] for __ in range(height)]


# Функция для вывода поля на экран
def draw_grid(canvas, grid):
	canvas.delete(tk.ALL)
	for y, row in enumerate(grid):
		for x, cell in enumerate(row):
			if cell:
				canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='white', outline='')


# Функция для расчёта следующего поколения
def next_generation(grid):
	new_grid = copy.deepcopy(grid)
	for y, row in enumerate(grid):
		for x, cell in enumerate(row):
			live_neighbors = 0
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					if dx == dy == 0:
						continue
					if grid[(y + dy) % len(grid)][(x + dx) % len(row)]:
						live_neighbors += 1
			if cell and (live_neighbors < 2 or live_neighbors > 3):
				new_grid[y][x] = 0
			elif not cell and live_neighbors == 3:
				new_grid[y][x] = 1
	return new_grid


# Функция для запуска игры
def run_game(width, height, delay=0.0001):
	root = tk.Tk()
	canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size, bg='black')
	canvas.pack()
	grid = init_grid(width, height)

	step_number = tk.Label(root, text='0', font=('Arial', 20), fg='red')
	step_number.place(relx=0.98, rely=0.02, anchor='center')

	fps = tk.Label(root, text='fps', font=('Arial', 20), fg='orange')
	fps.place(relx=0.07, rely=0.05, anchor='center')

	step = 0
	dt_prev = 0
	while True:
		t0 = time()

		step_number['text'] = str(step)
		draw_grid(canvas, grid)
		grid = next_generation(grid)
		sleep(delay)

		t1 = time()

		dt_cur = t1 - t0
		dt_mean = (dt_cur + dt_prev) / 2
		if step % 3 == 0:
			fps['text'] = str(round(1 / dt_mean, 1)) + '/' + str(round(1 / delay, 1)) + ' fps' + '\n' + str(round(1 / (dt_mean - delay), 1)) + ' fps'
		root.update()
		step += 1
		# save_as_png(canvas, './img/' + str(step))


# Запуск игры
if __name__ == "__main__":
	run_game(80, 40)
