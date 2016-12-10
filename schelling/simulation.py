import numpy as np
import numpy.random as rand
from .array_utils import get_agent_indices, get_vacancy_indices
from .neighborhood import get_unlike_neighbor_fraction
from .utility_functions import get_utility_for_array
from .create_array import create_array


def run_simulation(settings, callback=lambda arr, i: None):
	settings.validate()
	array = create_array(settings.grid_size, settings.get_agent_type_proportions())

	for i in range(settings.iterations):
		update_array(array, settings.utility_function, settings.satisficers)
		callback(array, i)


def update_array(array, utility_function, satisficers=False):
	# utility - function: (index) -> (0,1)
	utility = get_utility_for_array(utility_function, array)

	agent_indices = get_agent_indices(array)
	
	unsatisfied_agent_indices = _get_unsatisfied_agent_indices(utility, agent_indices)

	if unsatisfied_agent_indices.size == 0:
		return

	random_agent_index = _get_random_agent_index(agent_indices, unsatisfied_agent_indices)
	agent_utility = utility(random_agent_index)

	vacancies = get_vacancy_indices(array)

	better_vacancies = _get_better_vacancies(array, random_agent_index, utility, vacancies)

	if better_vacancies.size == 0:
		return

	random_better_vacancy = _get_random_better_vacancy_index(better_vacancies, vacancies)

	_move(array, random_agent_index, random_better_vacancy)


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


def _get_better_vacancies(array, agent_index, utility, vacancy_indices, satisficers=False):

	# TODO - when considering a vacancy, agents will include themselves in utility calculations:
	# if an agent moves to a vacancy in its own neighborhood, the utility of the spot he/she moved to
	# will change after the move. Currently the agent considers the pre-move 
	agent_utility = utility(agent_index)
	agent_type = array[tuple(agent_index)]

	def has_higher_utility(vacancy_index):
		return utility(tuple(vacancy_index), agent_type=agent_type) > agent_utility

	def has_higher_or_equal_utility(vacancy_index):
		return utility(tuple(vacancy_index), agent_type=agent_type) >= agent_utility

	if satisficers:
		better_vacancies = np.nonzero(np.apply_along_axis(has_higher_or_equal_utility, 1, vacancy_indices))[0]
	else:
		better_vacancies = np.nonzero(np.apply_along_axis(has_higher_utility, 1, vacancy_indices))[0]
	
	return better_vacancies


def _get_random_better_vacancy_index(better_vancancy_indices, vacancy_indices, random_chooser=rand.choice):
	if better_vancancy_indices.size != 0:
		i = random_chooser(better_vancancy_indices, 1)
		rand_better_vacancy_index = vacancy_indices[i][0]
		return rand_better_vacancy_index
	return None


def _move(array, agent_index, vacancy_index):
	agent_index = tuple(agent_index)
	vacancy_index = tuple(vacancy_index)

	array[vacancy_index] = array[agent_index]
	array[agent_index] = 0


if __name__ == '__main__':
	from .utility_functions import *
	from .arr_to_img import *
	from .simulation_settings import SimulationsSettings

	settings = SimulationsSettings(
			grid_size=100,
			vacancy_proportion=0.2,
			agent_proportions=(0.5, 0.5),
			utility_function=create_flat_utility(5/8),
			iterations=10000
		)

	save_period = 100

	def save(a, i):
		if i%save_period == 0:
			print(i)
			image_save(to_image(a), '../out/out'+str(i).zfill(6)+'.png')

	run_simulation(settings, callback=save)

