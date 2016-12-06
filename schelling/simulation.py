import numpy as np
import numpy.random as rand
from .array_utils import get_agent_indices, get_vacancy_indices
from .get_neighborhood import get_unlike_neighbor_fraction
from .utility_functions import get_utility_for_array

def run_simulation(array, utility_function, iterations, satisficers=False, callback=lambda arr, i: None):
	for i in range(iterations):
		array = update_array(array, utility_function)
		if array is None: print('none')
		callback(array, i)


def update_array(array, utility_function):
	# utility - function: (index) -> (0,1)
	utility = get_utility_for_array(utility_function, array)

	agent_indices = get_agent_indices(array)

	## f1
	def is_unsatisfied(index):
		return utility(tuple(index)) < 1.0

	unsatisfied_agent_indices = np.nonzero(np.apply_along_axis(is_unsatisfied, 1, agent_indices))[0]
	## /f1

	#print(unsatisfied_agent_indices)
	if unsatisfied_agent_indices.size == 0:
		return

	## get random agent utility
	random_agent_index = tuple(agent_indices[rand.choice(unsatisfied_agent_indices, 1)[0]])
	agent_utility = utility(random_agent_index)
	## / grau

	vacancies = get_vacancy_indices(array)

	## get better vacancies
	def has_higher_utility(vacancy_index):
		return utility(tuple(vacancy_index)) > agent_utility

	better_vacancies = np.nonzero(np.apply_along_axis(has_higher_utility, 1, vacancies))[0]
	## /gbv

	print(better_vacancies)

	## move to rand better vacancy
	if better_vacancies.size != 0:
		i = tuple(rand.choice(better_vacancies, 1))
		rand_better_vacancy_index = vacancies[i]

		_move(array, random_agent_index, rand_better_vacancy_index)

	## /mtrbv

	return array


def _get_unsatisfied_agent_indices(utility, agent_indices):
	"""Returns indices of unsatisfied agents - utility less than 1

	Args:
	    utility (Callable): functions to return utility given agent index
	    agent_indices (ndarray): 2d array with shape (x,2)

	Returns:
	    TYPE: indices of indices in agent_indices which point to unsatisfied agents
	"""
	def is_unsatisfied(index):
		return utility(tuple(index)) < 1.0

	unsatisfied_agent_indices = np.nonzero(np.apply_along_axis(is_unsatisfied, 1, agent_indices))[0]
	return unsatisfied_agent_indices


def _get_random_agent_index(agent_indices, unsatisfied_agent_indices, random_chooser=rand.choice):
	# random chooser is a parameter only for testing
	random_agent_index = tuple(agent_indices[random_chooser(unsatisfied_agent_indices, 1)[0]])
	return random_agent_index


def _get_better_vacancies(array, agent_index, utility, vacancy_indices):

	# TODO - when considering a vacancy, agents will include themselves in utility calculations:
	# if an agent moves to a vacancy in its own neighborhood, the utility of the spot he/she moved to
	# will change after the move. Currently the agent considers the pre-move 
	agent_utility = utility(agent_index)
	agent_type = array[tuple(agent_index)]

	def has_higher_utility(vacancy_index):
		return utility(tuple(vacancy_index), agent_type=agent_type) > agent_utility

	better_vacancies = np.nonzero(np.apply_along_axis(has_higher_utility, 1, vacancy_indices))[0]
	return better_vacancies


def _get_random_better_vacancy_index(better_vancancy_indices, vacancy_indices, random_chooser=rand.choice):
	if better_vancancy_indices.size != 0:
		i = random_chooser(better_vancancy_indices, 1)
		rand_better_vacancy_index = vacancy_indices[i]
		return rand_better_vacancy_index
	return None



def _move(array, agent_index, vacancy_index):
	#agents move to first better vacancy on list
	print('move ', agent_index, ' ', vacancy_index)
	agent_index = tuple(agent_index)
	vacancy_index = tuple(vacancy_index)

	array[agent_index], array[vacancy_index] = array[vacancy_index], array[agent_index]


# if __name__ == '__main__':
# 	from .create_array import create_array
# 	from .utility_functions import *
# 	import os
# 	import time
# 	from .arr_to_img import *

# 	np.set_printoptions(threshold=np.nan)

# 	def swap(arr):
# 		arr[0, 0], arr[0, 1] = arr[0, 1], arr[0, 0]


# 	arr = create_array(20, (0.2, 0.4, 0.4))
# 	print(arr)
# 	swap(arr)
# 	print(arr)


# 	def pnt(a, i):
# 			os.system("clear")
# 			print(a, i)

# 	def save(a, i):
# 		if i%100 == 0:
# 			print(i)
# 			image_save(to_image(a), '../out/out'+str(i).zfill(6)+'.png')

# 	run_simulation(arr, create_flat_utility(0.9), 10000, callback=save)