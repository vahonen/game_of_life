# -*- coding: cp1252 -*-

from sense_hat import SenseHat
import random
import time

sense = SenseHat()

def initialize(pixel_list, nbr_of_pixels):
	
	sense.clear()
	for y in range(8):
		for x in range(8):
			pixel_list[y][x] = 0
		
	
	r=random.randrange(255)
	g=random.randrange(255)
	b=random.randrange(255)
	
	while True:
		rnd_x = random.randint(0,7)
		rnd_y = random.randint(0,7)
		if pixel_list[rnd_y][rnd_x] == 0:
			sense.set_pixel(rnd_x, rnd_y, (r,g,b))
			nbr_of_pixels -= 1
			pixel_list[rnd_y][rnd_x] = 1
			if nbr_of_pixels == 0:
				break

def count_neighbours(pixel_list, y, x):
	neighbours = 0
	for yy in range(y-1, y+2):
		for xx in range(x-1, x+2):
			if (yy >= 0 and yy <= 7 and xx >= 0 and xx <= 7):
				if (yy != y or xx != x):
					if pixel_list[yy][xx] == 1:
						neighbours += 1
	
	return neighbours

# Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.		
# lähde: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

def next_gen(pixel_list):
	new_count = 0
	tmp_pixel_list = [[0] * 8 for i in range(8)]
	for y in range(8):
		for x in range(8):
			neighbours = count_neighbours(pixel_list, y, x)
			
			if pixel_list[y][x] == 0:
				if neighbours == 3:
					tmp_pixel_list[y][x] = 1
					new_count += 1
			else:
				if (neighbours < 2 or neighbours > 3):
					tmp_pixel_list[y][x] = 0
				else:
					tmp_pixel_list[y][x] = 1
					new_count += 1
	
	if new_count == 0:
		return new_count
			
	for y in range(8):
		for x in range(8):
			pixel_list[y][x] = tmp_pixel_list[y][x]
	
	return new_count	

def display_pixels(pixel_list):
	
	r=random.randrange(255)
	g=random.randrange(255)
	b=random.randrange(255)
	for y in range(8):
		for x in range(8):
			if pixel_list[y][x] == 1:
				sense.set_pixel(x, y, (r,g,b))
			else:
				sense.set_pixel(x, y, (0,0,0))

def destroy(pixel_list):
	for rounds in range(10):
		for y in range(8):
			for x in range(8):
				if pixel_list[y][x] == 1:
					if rounds % 2 == 0:
						sense.set_pixel(x, y, (255,255,0))
					else:
						sense.set_pixel(x, y, (255,0,0))
		time.sleep(0.1)
		
def main():
	pixel_count = 10
	pixel_list = [[0] * 8 for i in range(8)]
	initialize(pixel_list, pixel_count)
	old_count = pixel_count
	new_count = 0
	stop_level = 0

	while True:
		display_pixels(pixel_list)
		time.sleep(1)
		new_count = next_gen(pixel_list)
		if (new_count == old_count):
			stop_level += 1
		else:
			stop_level = 0
			
		if (stop_level > 5 or new_count == 0):
			sense.clear()
			destroy(pixel_list)
			initialize(pixel_list, pixel_count)
			old_count = pixel_count
			new_count = 0
			stop_level = 0
		old_count = new_count
	
if __name__ == "__main__":
	main()