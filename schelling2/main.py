import math
import numpy as np
import scipy.ndimage as si
import itertools
import os
import multiprocessing

from schelling.create_array import create_array
from schelling.segregation_measures import unlike_neighbor_fraction_average_ncv

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
	satisfactory_vacancies = np.argwhere(array_where_vacant & (unlike[agent_t-1] <= th[agent_t-1]))
	if len(satisfactory_vacancies)!=0:
		move_to_index = tuple(satisfactory_vacancies[np.random.choice(satisfactory_vacancies.shape[0])])
		array[move_to_index] = 1
		array[agent_to_move_index] = 0

	return False

def run_simulation(v, th):
	i = 1

	p=(v,(1-v)/2,(1-v)/2)
	arr = create_array(size	,p)

	# sim_state = dict()
	status = None

	while True:
		# what if satisfied at i % 100 == 0 ???
		done = run_iteration(arr, th)
		if done:
			# print(arr)
			status = "Satisfied"
			# sim_state[str(i)] = np.copy(arr)
			break
		if i % 100 == 0:
			# print(i)
			# print(arr)
			# sim_state[str(i)] = np.copy(arr)
			if check_halted(arr, th):
				status = "Frozen"
				break

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
	save_path = os.path.join(output_dir, name)


	if os.path.isfile(save_path):
		print("skipping: " + name)
		return

	result = run_simulation(*run_settings[:-1])
	
	np.save(save_path, result[0])

	final_state = result[1]
	final_unf = result[2]
	final_i = result[3]

	append_result_csv(v, th0, th1, no, final_state, str(final_unf), str(final_i))
	print(name)
	return result
	

if __name__ == '__main__':

	vs = np.arange(0,1,.01)	

	th = list()

	for t0 in range(9):
		for t1 in range(t0, 9):
			th.append((t0,t1))
	# print(len(th))
	# exit()
	nos = range(10)

	settings = itertools.product(vs, th, nos)

	# import random
	# random.seed(20)
	# settings = random.sample(list(sorted(settings)),20)
	# for seed 10, sample 20 
	# 1000 = 186s
	# 100 = 201s
	# for seed 10, sample 100
	# 1000 = 592s 
	# 100 = 556s

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

	
	

