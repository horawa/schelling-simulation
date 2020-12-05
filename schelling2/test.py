import numpy as np
import math


def get_nearest_vacancy(x, y, th, size, unlike):
	# TODO: Figure out how to do this in numpy.
	# get nearest satisfactory vacancy (manhattan distance)
	# diamond spiral pattern from x,y traverses by order of manhattan distance

	x0, y0 = x, y

	unlike[x,y] = 2

	dirs = [(0, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)]

	# is_satisfied = unlike[x,y] <= th
	
	dist = 0
	steps = 0
	dir_ = len(dirs) - 1

	while True:
		# up 1
		# dir = (-1, 1), steps = dist -1
		# dir = (-1, -1), steps = dist
		# dir = (1, -1), steps = dist
		# dir = (1, 1), steps = dist
		if steps == 0:
			if dir_ == (len(dirs) - 1):
				dist += 1
				dir_ = 0
				steps = 1
			else: 
				dir_ += 1
				if dir_ == 1:
					steps = dist -1
				else:
					steps = dist
			continue

		x += dirs[dir_][0]
		y += dirs[dir_][1]
		steps -= 1
		# if is satisfied 

		if x < 0 or y < 0 or x >= size or y >= size:
			if abs(y-y0) > 2*size:
				break
			else:
				# print(x, y)
				continue

		unlike[x,y] = 1
		# print(abs(x-x0) + abs(y-y0))
		# print(unlike)

		# if unlike[x,y] <= th:
		# 	return (x, y)

	return None

if __name__ == '__main__':
	size = 101
	unlike = np.zeros((size, size))
	# x, y = size // 2, size // 2
	x, y = size-1, size-1
	get_nearest_vacancy(x, y, 0, size, unlike)

	print(np.all(unlike))

	unlike = np.zeros((size, size))
	# x, y = size // 2, size // 2
	x, y = 0, size-1
	get_nearest_vacancy(x, y, 0, size, unlike)

	print(np.all(unlike))

	unlike = np.zeros((size, size))
	# x, y = size // 2, size // 2
	x, y = size-1, 0
	get_nearest_vacancy(x, y, 0, size, unlike)

	print(np.all(unlike))


	unlike = np.zeros((size, size))
	# x, y = size // 2, size // 2
	x, y = 0, 0
	get_nearest_vacancy(x, y, 0, size, unlike)

	print(np.all(unlike))

	unlike = np.zeros((size, size))
	x, y = size // 2, size // 2
	
	get_nearest_vacancy(x, y, 0, size, unlike)

	print(np.all(unlike))

	unlike = np.zeros((size, size))
	for i in range(1000):
		x, y = 50,50
		
		get_nearest_vacancy(x, y, 0, size, unlike)

		# print(np.all(unlike))

