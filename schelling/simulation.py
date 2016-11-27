import numpy as np
from numpy.random import randint, choice
from .array_utils import get_agent_indices, get_vacancy_indices
from .get_neighborhood import get_unlike_neighbor_fraction

def run_simulation(array, utility_function, iterations, satisficers=False, callback=lambda arr, i: None):
	for i in range(iterations):
		update_array(array, utility_function)
		callback(array, i)


def update_array(array, utility_function):
	def utility(index):
		return utility_function(get_unlike_neighbor_fraction(array, index))

	agent_indices = get_agent_indices(array)
	random_agent_index = tuple(agent_indices[randint(0, agent_indices.shape[0])])
	agent_utility = utility(random_agent_index)

	vacancies = get_vacancy_indices(array)


	def has_higher_utility(vacancy_index):
		return utility(tuple(vacancy_index)) > agent_utility

	better_vacancies = np.nonzero(np.apply_along_axis(has_higher_utility, 1, vacancies))[0]
	if better_vacancies.size != 0:
		i = tuple(choice(better_vacancies, 1))
		rand_better_vacancy_index = vacancies[i]

		_move(array, random_agent_index, rand_better_vacancy_index)



def _move(array, agent_index, vacancy_index):
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

# 	arr = create_array(20, (0.2, 0.4, 0.4))
# 	def pnt(a, i):
# 			os.system("clear")
# 			print(a, i)

# 	def save(a, i):
# 		if i%100 == 0:
# 			print(i)
# 			image_save(to_image(a), '../out/out'+str(i)+'.png')

# 	run_simulation(arr, create_flat_utility(0.5), 10000, callback=save)