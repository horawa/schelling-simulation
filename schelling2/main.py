import math
import numpy as np
import scipy.ndimage as si
import itertools
import os
import multiprocessing

from schelling.create_array import create_array
from schelling.segregation_measures import unlike_neighbor_fraction_average_ncv
from schelling.arr_to_img import image_save, to_image

threads = 8
size = 100
output_dir = os.path.join(os.path.expanduser("~"),"results_2020")
output_csv = os.path.join(output_dir,"result.csv")

def append_result_csv(*row):
	with open(output_csv, "a+") as csv:
		csv.write(",".join(row)+"\n")

# def get_unsatisfied(array, th)
# 	schelling_filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
	
# 	array_where_vacant = (array==0)
# 	agent_type = [None, None]
# 	agent_type[0] = (array==1)
# 	agent_type[1] = (array==2)
	
# 	# print(array)
# 	# print(array_where_vacant)

# 	unlike = [None, None]
# 	unlike[0] = si.convolve(agent_type[1].astype(int), schelling_filter, mode='wrap')
# 	unlike[1] = si.convolve(agent_type[0].astype(int), schelling_filter, mode='wrap')

# 	unsatisfied = (agent_type[0] & (unlike[0]>th)) | (agent_type[1] & (unlike[1]>th))

# 	return unsatisfied

# def get_unlike(array):
# 	unlike = [None, None]
# 	unlike[0] = si.convolve(agent_type[1].astype(int), schelling_filter, mode='wrap')
# 	unlike[1] = si.convolve(agent_type[0].astype(int), schelling_filter, mode='wrap')

# 	return unlike

def check_halted(array, th):
	schelling_filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
	
	array_where_vacant = (array==0)
	agent_type = [None, None]
	agent_type[0] = (array==1)
	agent_type[1] = (array==2)
	
	# print(array)
	# print(array_where_vacant)

	unlike = [None, None]
	unlike[0] = si.convolve(agent_type[1].astype(int), schelling_filter, mode='wrap')
	unlike[1] = si.convolve(agent_type[0].astype(int), schelling_filter, mode='wrap')

	unsatisfied = [None, None]
	unsatisfied[0] = (agent_type[0] & (unlike[0]>th[0]))
	unsatisfied[1] = (agent_type[1] & (unlike[1]>th[1]))

	satisfactory_vacancies = [None, None]
	satisfactory_vacancies[0] = array_where_vacant & (unlike[0] <= th[0])
	satisfactory_vacancies[1] = array_where_vacant & (unlike[1] <= th[1])

	has_unsatisfied = [np.any(unsatisfied[n]) for n in [0,1]]
	has_satisfactory = [np.any(satisfactory_vacancies[n]) for n in [0,1]]

	can_move = [has_unsatisfied[n] and has_satisfactory[n] for n in [0,1]]

	return not (can_move[0] or can_move[1])



def run_iteration(array, th=[5,5]):
	schelling_filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
	
	array_where_vacant = (array==0)
	agent_type = [None, None]
	agent_type[0] = (array==1)
	agent_type[1] = (array==2)
	
	# print(array)
	# print(array_where_vacant)

	unlike = [None, None]
	unlike[0] = si.convolve(agent_type[1].astype(int), schelling_filter, mode='wrap')
	unlike[1] = si.convolve(agent_type[0].astype(int), schelling_filter, mode='wrap')

	unsatisfied = np.argwhere((agent_type[0] & (unlike[0]>th[0])) | (agent_type[1] & (unlike[1]>th[1])))
	if len(unsatisfied)==0:
		return True
	
	agent_to_move_index = tuple(unsatisfied[np.random.choice(unsatisfied.shape[0])])
	
	agent_t = array[agent_to_move_index]

	x, y = agent_to_move_index
	move_to_index = get_nearest_vacancy(x, y, th[agent_t-1], size, array, unlike[agent_t - 1])
	if move_to_index:
		array[move_to_index] = agent_t
		array[agent_to_move_index] = 0

	# satisfactory_vacancies = np.argwhere(array_where_vacant & (unlike[agent_t-1] <= th[agent_t-1]))
	# if len(satisfactory_vacancies)!=0:
	# 	move_to_index = tuple(satisfactory_vacancies[np.random.choice(satisfactory_vacancies.shape[0])])
	# 	array[move_to_index] = 1
	# 	array[agent_to_move_index] = 0

	return False

def check_halted_own_group_th(array, th):
	schelling_filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
	
	array_where_vacant = (array==0)
	agent_type = [None, None]
	agent_type[0] = (array==1)
	agent_type[1] = (array==2)
	
	# print(array)
	# print(array_where_vacant)


	own_group_count = [None, None]
	own_group_count[0] = si.convolve(agent_type[0].astype(np.int8), schelling_filter, mode='constant', cval=0)
	own_group_count[1] = si.convolve(agent_type[1].astype(np.int8), schelling_filter, mode='constant', cval=0)

	neigbor_count = si.convolve(np.logical_not(array_where_vacant).astype(np.int8), schelling_filter, mode='constant', cval=0).astype(float)

	own_group_rel = [None, None]
	own_group_rel[0] = np.true_divide(own_group_count[0].astype(float), neigbor_count.astype(float), out=np.zeros_like(neigbor_count), where=neigbor_count!=0)
	own_group_rel[1] = np.true_divide(own_group_count[1].astype(float), neigbor_count.astype(float), out=np.zeros_like(neigbor_count), where=neigbor_count!=0)
	
	unsatisfied = [None, None]
	unsatisfied[0] = (agent_type[0] & (own_group_rel[0]<th[0]))
	unsatisfied[1] = (agent_type[1] & (own_group_rel[1]<th[1]))

	satisfactory_vacancies = [None, None]
	satisfactory_vacancies[0] = array_where_vacant & (own_group_rel[0] >= th[0])
	satisfactory_vacancies[1] = array_where_vacant & (own_group_rel[1] >= th[1])

	has_unsatisfied = [np.any(unsatisfied[n]) for n in [0,1]]
	has_satisfactory = [np.any(satisfactory_vacancies[n]) for n in [0,1]]

	can_move = [has_unsatisfied[n] and has_satisfactory[n] for n in [0,1]]

	return not (can_move[0] or can_move[1])

def run_iteration_own_group_th(array, th=[5,5]):
	schelling_filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
	
	array_where_vacant = (array==0)
	agent_type = [None, None]
	agent_type[0] = (array==1)
	agent_type[1] = (array==2)
	
	# print(array)
	# print(array_where_vacant)

	own_group_count = [None, None]
	own_group_count[0] = si.convolve(agent_type[0].astype(np.int8), schelling_filter, mode='constant', cval=0)
	own_group_count[1] = si.convolve(agent_type[1].astype(np.int8), schelling_filter, mode='constant', cval=0)

	neigbor_count = si.convolve(np.logical_not(array_where_vacant).astype(np.int8), schelling_filter, mode='constant', cval=0).astype(float)

	own_group_rel = [None, None]
	own_group_rel[0] = np.true_divide(own_group_count[0].astype(float), neigbor_count.astype(float), out=np.zeros_like(neigbor_count), where=neigbor_count!=0)
	own_group_rel[1] = np.true_divide(own_group_count[1].astype(float), neigbor_count.astype(float), out=np.zeros_like(neigbor_count), where=neigbor_count!=0)

	unsatisfied = np.argwhere((agent_type[0] & (own_group_rel[0]<th[0])) | (agent_type[1] & (own_group_rel[1]<th[1])))
	if len(unsatisfied)==0:
		return True
	
	agent_to_move_index = tuple(unsatisfied[np.random.choice(unsatisfied.shape[0])])
	
	agent_t = array[agent_to_move_index]

	# x, y = agent_to_move_index
	# move_to_index = get_nearest_vacancy(x, y, th[agent_t-1], size, array, unlike[agent_t - 1])
	# if move_to_index:
	# 	array[move_to_index] = agent_t
	# 	array[agent_to_move_index] = 0

	satisfactory_vacancies = np.argwhere(array_where_vacant & (own_group_rel[agent_t-1] >= th[agent_t-1]))
	if len(satisfactory_vacancies)!=0:
		move_to_index = tuple(satisfactory_vacancies[np.random.choice(satisfactory_vacancies.shape[0])])
		array[move_to_index] = agent_t
		array[agent_to_move_index] = 0

	return False

def run_simulation(v, th, imdir):
	i = 1

	p=(v,(1-v)/2,(1-v)/2)
	arr = create_array(size	,p)

	# sim_state = dict()
	status = None

	while True:
		# what if satisfied at i % 100 == 0 ???
		done = run_iteration_own_group_th(arr, th)
		if done:
			# print(arr)
			status = "Satisfied"
			# sim_state[str(i)] = np.copy(arr)
			break
		if i % 100 == 0:
			# print(i)
			# print(arr)
			# sim_state[str(i)] = np.copy(arr)
			# image_save(to_image(arr), os.path.join(imdir, str(i)+".png"))
			if check_halted_own_group_th(arr, th):
				status = "Frozen"
				break
			# print(i)

		i += 1

	unf = unlike_neighbor_fraction_average_ncv(arr, np.argwhere(arr != 0))

	sim_state = (arr, status, unf, i)

	return sim_state

	# # print(array[agent_to_move_index])
	# for i_ag in [0,1]:
	# 	if(array[agent_to_move_index]==(i_ag-1)):
	# 		satisfactory_vacancies = np.argwhere(array_where_vacant & (unlike1 <= th))
	# 		if len(satisfactory_vacancies)==0:
	# 			return array
	# 		move_to_index = tuple(satisfactory_vacancies[np.random.choice(satisfactory_vacancies.shape[0])])
	# 		array[move_to_index] = 1
	# 		array[agent_to_move_index] = 0

	# if(array[agent_to_move_index]==1):
	# 	satisfactory_vacancies = np.argwhere(array_where_vacant & (unlike1 <= th))
	# 	if len(satisfactory_vacancies)==0:
	# 		return array
	# 	move_to_index = tuple(satisfactory_vacancies[np.random.choice(satisfactory_vacancies.shape[0])])
	# 	array[move_to_index] = 1
	# 	array[agent_to_move_index] = 0
	# else:
	# 	satisfactory_vacancies = np.argwhere(array_where_vacant & (unlike2 <= th))
	# 	if len(satisfactory_vacancies)==0:
	# 		return array
	# 	move_to_index = tuple(satisfactory_vacancies[np.random.choice(satisfactory_vacancies.shape[0])])
	# 	array[move_to_index] = 2

def sim_thread(run_settings):
	

	v = "%.2f" % run_settings[0]
	th0 = str(run_settings[1][0])
	th1 = str(run_settings[1][1])
	no = str(run_settings[2])
	
	name = "_".join([v,th0,th1,no])+".npy"
	imdir = os.path.join(output_dir, "_".join([v,th0,th1,no]))
	# os.mkdir(imdir)
	save_path = os.path.join(output_dir, name)


	if os.path.isfile(save_path):
		print("skipping: " + name)
		return

	result = run_simulation(*(list(run_settings[:-1])+[imdir]))
	
	np.save(save_path, result[0])

	final_state = result[1]
	final_unf = result[2]
	final_i = result[3]

	append_result_csv(v, th0, th1, no, final_state, str(final_unf), str(final_i))
	print(name)
	return result
	

# def get_nearest_vacancy(x, y, agent_t, th, size, unlike):
# 	# TODO: Figure out how to do this in numpy.
# 	# get nearest satisfactory vacancy (manhattan distance)
# 	# spiral pattern from x,y

# 	dirs = [(0, 1), (-1, 1), (-1, 1), (1, 1)]

# 	dist = 1
# 	is_satisfied = unlike[x,y] <= th

# 	while True:
# 		# up 1
# 		# dir = (-1, 1), steps = dist -1
# 		# dir = (-1, -1), steps = dist
# 		# dir = (-1, 1), steps = dist
# 		# dir = (1, 1), steps = dist
# 		if steps == 0:
# 			if dir_ == (len(dirs) - 1):
# 				dist += 1
# 				dir_ = 0
# 				steps = 1
# 			else: 
# 				dir_ += 1
# 				if dir_ == 0:
# 					steps = dist -1
# 				else:
# 					steps = dist

# 		x, y += *dirs[dir_]
# 		steps -= 1
# 		# if is satisfied 

# 		if x < 0 or y < 0 or x >= size or y >= size:
# 			continue

# 		if unlike[x,y] <= th:
# 			return (x, y)
# 
	# return None

def get_nearest_vacancy(x, y, th, size, array, unlike):
	# TODO: Figure out how to do this in numpy.
	# get nearest satisfactory vacancy (manhattan distance)
	# diamond spiral pattern from x,y traverses by order of manhattan distance

	x0, y0 = x, y

	dirs = [(0, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)]
	
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

		if x < 0 or y < 0 or x >= size or y >= size:
			if abs(y-y0) > 2*size:
				break
			else:
				continue

		# if satisfactory
		# print(type(array[(x,y)]))
		if (int(array[(x,y)]) == 0) and (int(unlike[(x,y)]) <= th):
			return (x, y)

	return None

		# move up
		# move up and then left by dist-1
		# move down left by dist
		# move down right by dist
		# move up right by dist




if __name__ == '__main__':

	vs = np.arange(0,1,.01)	

	th = list()

	for t0 in range(9):
		for t1 in range(t0, 9):
			th.append((t0/8,t1/8))
	# print(len(th))
	# exit()
	nos = range(10)

	settings = itertools.product(vs, th, nos)

	# print(len(list(sorted(settings))))
	# = 45000

	# import random
	# random.seed(20)
	# settings = random.sample(list(sorted(settings)),20)
	# for seed 10, sample 20 
	# 1000 = 186s
	# 100 = 201s
	# for seed 10, sample 100
	# 1000 = 592s 
	# 100 = 556s
	# import random
	# random.seed(20)
	# settings = random.sample(list(sorted(settings)),100)
	# agents move to nearest vacancy


	with multiprocessing.Pool(threads) as pool:
		pool.map(sim_thread, settings)


	# for setting in settings:
	# 	result = run_simulation(*setting[:-1])
	# 	# v = str(setting[0])[:5]
	# 	v = "%.2f" % setting[0]
	# 	th0 = str(setting[1][0])
	# 	th1 = str(setting[1][1])
	# 	no = str(setting[2])
	# 	name = "_".join([v,th0,th1,no])+".npy"
	# 	np.save(os.path.join(output_dir, name), result[0])

	# 	print(name)

	# print(len(list(settings)))


	# unf = unlike_neighbor_fraction_average_ncv(arr, np.argwhere(arr != 0))
	# print(unf)

	# 1315 at 1440

	
	

