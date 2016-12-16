import numpy as np
import numpy.random as rand
import math
import os

from .array_utils import get_agent_indices, get_vacancy_indices
from .neighborhood import get_unlike_neighbor_fraction
from .utility_functions import get_utility_for_array
from .create_array import create_array
from .simulation_result import SimulationResult
from .arr_to_img import to_image, image_save
import schelling.segregation_measures as sm


def run_simulation(settings, callback=lambda arr, res, i: None):
	"""Run simulation with specified settings.
	Call the optional callback function after each iteration,
	passing the current array state, current result, and iteration number.
	Returns simulation result - segregation measures before each iteration.
	
	Args:
	    settings (SimulationSettings): settings
	    callback (callable, optional): Function to call after each iteration
	
	Returns:
	    SimulationResult: Result - segregation measures for each iteration
	"""
	settings.validate()
	result = SimulationResult()

	array = create_array(settings.grid_size, 
		settings.get_agent_type_proportions(), 
		settings.initial_random_allocation)

	# utility - function: (index) -> (0,1)
	utility = get_utility_for_array(settings.utility_function, array, 
		count_vacancies=settings.count_vacancies)

	pickers = {
		'random': _random_picker,
		'first': _first_picker,
	}

	agent_pickers = dict(pickers, **{
		'roulette': _create_roulette_picker(
			settings.agent_roulette_base_weight, utility, for_agents=True),
	})

	vacancy_pickers = dict(pickers, **{
		'roulette': _create_roulette_picker(
			settings.vacancy_roulette_base_weight, utility, for_agents=False),
	})

	agent_picker = agent_pickers[settings.agent_picking_regime]
	vacancy_picker = vacancy_pickers[settings.vacancy_picking_regime]

	for i in range(settings.iterations):
		callback(array, result, i)
		is_simulation_halted = update_array(array, utility, settings.radius, 
			result, agent_picker, vacancy_picker, settings.count_vacancies, 
			settings.satisficers)

		# if no further moves are possible, exit simulation early
		if is_simulation_halted:
			break

	return result


def update_array(array, utility, radius, result, agent_picker, 
	vacancy_picker, count_vacancies, satisficers=False):
	"""Do a single iteration of the simulation.
	
	Args:
	    array (ndarray): array
	    utility (callable): utility function - (agent index) -> (0, 1)
	    radius (int): neighborhood radius
	    result (SimulationResult): result object to store segregation measures 
	    	before updating array
	    satisficers (bool, optional): satisficer behavior setting
	"""
	agent_indices = get_agent_indices(array)

	_update_result(result, array, agent_indices, count_vacancies)
	
	unsatisfied_agent_indices = _get_unsatisfied_agent_indices(utility, 
		agent_indices, satisficers=satisficers)

	# if all agents satisfied, end simulation
	if unsatisfied_agent_indices.size == 0:
		return True

	agent_index = _pick_agent_index_to_move(unsatisfied_agent_indices, 
		agent_picker)
	agent_utility = utility(agent_index)

	vacancy_indices = get_vacancy_indices(array)

	# if vacancy picker is roulette, consider all vacancies 
	if vacancy_picker.__name__ == 'roulette_picker':
		better_vacancy_indices = vacancy_indices
	else:
		better_vacancy_indices = _get_better_vacancies(array, agent_index, 
			utility, vacancy_indices, satisficers=satisficers)

	if better_vacancy_indices.size == 0:
		# if relocation regime is move first, and the first agent has no better
		# vacancy, the simulation will halt. If this happens, try all
		# unsatisfied agents in list and pick the first one which can find a
		# better vacancy. If none have a better vacancy, end the simulation.
		if agent_picker is _first_picker:
			for agent_index in unsatisfied_agent_indices:
				better_vacancy_indices = _get_better_vacancies(array, 
					agent_index, utility, vacancy_indices, 
					satisficers=satisficers)

				if better_vacancy_indices.size != 0:
					break
			else:
				return True
		else:
			return False
	agent_type = array[agent_index]	
	better_vacancy = _pick_better_vacancy_index(better_vacancy_indices, 
		vacancy_picker, agent_type)

	_move(array, agent_index, better_vacancy)

	return False


def _get_unsatisfied_agent_indices(utility, agent_indices, satisficers=False):
	"""Returns indices of unsatisfied agents - utility less than 1

	Args:
	    utility (callable): functions to return utility given agent index
	    agent_indices (ndarray): 2d array with shape (x,2)

	Returns:
	    ndarray: indices of rows in agent_indices which point to unsatisfied 
	    	agents
	"""
	def is_unsatisfied(index):
		return utility(tuple(index)) < 1.0

	if satisficers:
		# if satisficers all agents are potentially unsatisfied
		unsatisfied_agent_index_indices = np.arange(0, agent_indices.shape[0])
	else:
		unsatisfied_agent_index_indices = np.nonzero(np.apply_along_axis(
			is_unsatisfied, 1, agent_indices))[0]
	return agent_indices[unsatisfied_agent_index_indices]


def _pick_agent_index_to_move(unsatisfied_agent_indices, 
	agent_picker):
	"""Get index of random unsatisfied agent in agent indices.
	
	Args:
	    unsatisfied_agent_indices (ndarray): indices of unsatisfied agents in 
	    	array
	    agent_picker (callable, optional): function to return random row 
	    	from array
	
	Returns:
	    tuple: Index of random unsatisfied agent
	"""
	agent_index = tuple(agent_picker(unsatisfied_agent_indices))
	return agent_index


def _get_better_vacancies(array, agent_index, utility, vacancy_indices, 
	satisficers=False):
	"""Get vacancies of higher utility for agent at agent_index.
	If satisficers is True, also returns vacancies of equal utility.
	
	Args:
	    array (ndarray): array
	    agent_index (tuple): index of agent
	    utility (callable): utility function - index -> (0, 1)
	    vacancy_indices (ndarray): indices vacancies in array
	    satisficers (bool, optional): satisficers setting
	
	Returns:
	    ndarray: array containtig incices of rows in vacancy_indices pointing 
	    	to vacancies of higher utility.
	"""
	# TODO - when considering a vacancy, agents will include themselves 
	# in utility calculations: if an agent moves to a vacancy in its own 
	# neighborhood, the utility of the spot he/she moved to will change after 
	# the move. Currently the agent considers the pre-move 
	agent_utility = utility(agent_index)
	agent_type = array[tuple(agent_index)]

	def has_higher_utility(vacancy_index):
		return utility(tuple(vacancy_index), 
			agent_type=agent_type) > agent_utility

	def has_equal_utility(vacancy_index):
		return math.isclose(utility(tuple(vacancy_index), 
			agent_type=agent_type), agent_utility)

	better_vacancy_index_indices = np.nonzero(np.apply_along_axis(
		has_higher_utility, 1, vacancy_indices))[0]

	# if satisficers, and no better vacancy exists
	if better_vacancy_index_indices.size == 0 and satisficers:
		better_vacancy_index_indices = np.nonzero(
			np.apply_along_axis(has_equal_utility, 1, vacancy_indices))[0]

	return vacancy_indices[better_vacancy_index_indices]


def _pick_better_vacancy_index(better_vancancy_indices, 
		vacancy_picker, agent_type=None):
	"""Get random index of row in vacancy indices pointing to better vacancy
	
	Args:
	    better_vancancy_indices (ndarray): indices of rows in vacancy indices 
	    	pointing to better vacancies
	    vacancy_indices (ndarray): indices of vacancies
	    vacancy_picker (callable, optional):  function to return number 
	    	from array
	
	Returns:
	    tuple: random better vacancy index
	"""
	if better_vancancy_indices.size != 0:
		better_vacancy_index = vacancy_picker(better_vancancy_indices, 
			agent_type)
		return better_vacancy_index
	return None


def _move(array, agent_index, vacancy_index):
	"""Swap agent at agent_index and vacancy at vacancy_index in array"""
	agent_index = tuple(agent_index)
	vacancy_index = tuple(vacancy_index)

	array[vacancy_index] = array[agent_index]
	array[agent_index] = 0


def _update_result(result, array, agent_indices, count_vacancies):
	"""Store current segregation measures in segregation result object
	
	Args:
	    result (SegregationResult): result object
	    array (ndarray): array
	    agent_indices (ndarray): indices of agents in array
	"""
	switch_rate_average = sm.switch_rate_average(array, agent_indices)
	entropy_average = sm.entropy_average(array, agent_indices, 
		count_vacancies=count_vacancies)
	ghetto_rate = sm.ghetto_rate(array, agent_indices)
	clusters = sm.clusters(array)
	distance_average = sm.distance_average(array, agent_indices)
	mix_deviation_average = sm.mix_deviation_average(array, agent_indices)
	share_average = sm.share_average(array, agent_indices)

	result.switch_rate_average.append(switch_rate_average)
	result.entropy_average.append(entropy_average)
	result.ghetto_rate.append(ghetto_rate)
	result.clusters.append(clusters)
	result.distance_average.append(distance_average)
	result.mix_deviation_average.append(mix_deviation_average)
	result.share_average.append(share_average)


def _first_picker(agent_indices, agent_type=None):
	return tuple(agent_indices[0])


def _random_picker(agent_indices, agent_type=None):
	rand_index_index = rand.randint(0, agent_indices.shape[0])
	return tuple(agent_indices[rand_index_index])


def _create_roulette_picker(base_weight, utility, for_agents=True, 
	uniform_dist=rand.uniform):
	"""Agents will be assigned the weight of 1 - utility + base_weight
	Vacancies will be assigned the weight of utility + base_weight"""

	def roulette_picker(array_indices, agent_type=None):
		
		utilities = np.apply_along_axis(utility, 1, array_indices, 
			agent_type=agent_type)
		total_utilities = np.sum(utilities)
		
		sorted_utility_indices = np.argsort(utilities)

		if for_agents:
			total_weights = (
				utilities.size * (1 + base_weight)) - total_utilities
		else:
			total_weights = (utilities.size * base_weight) + total_utilities
		
		picked_total = uniform_dist(total_weights)

		current_total_weight = 0
		for index in sorted_utility_indices:
			if for_agents:
				weight = 1 - utilities[index] + base_weight
			else:
				weight = utilities[index] + base_weight

			current_total_weight += weight

			if current_total_weight >= picked_total:
				return tuple(array_indices[index])

		# if picked value out of range (float error), pick last index
		return tuple(array_indices[sorted_utility_indices[-1]])
	return roulette_picker


def get_save_state_callback(save_directory, save_period, 
		iterations, verbose=False):
	iter_order_of_magnitude = int(math.log10(iterations))
	def save_state(array, result, iteration):
		if iteration % save_period == 0:
			file_name = str(iteration).zfill(iter_order_of_magnitude) + '.png'
			image_save(to_image(array), 
				os.path.join(save_directory, file_name))
			if verbose:
				print(iteration)
				print(result)
	return save_state


if __name__ == '__main__': # pragma: no cover
	"""
	This will run the Schelling Model simulation for 10000 iterations.
	Every 100 iterations the state will be printed to console  and the array 
	will be saved as an image.
	The simulation result, containing segregation measures for each iteration
	will be saved as JSON and a plot will be shown.
	"""
	from schelling.simulation import run_simulation, get_save_state_callback
	from schelling.utility_functions import create_flat_utility
	from schelling.arr_to_img import image_save, to_image
	from schelling.simulation_settings import SimulationSettings
	import os

	settings = SimulationSettings(
			grid_size=40,
			vacancy_proportion=0.2,
			agent_proportions=(0.5, 0.5),
			utility_function=create_flat_utility(5/8),
			iterations=10000
		)

	save_period = 100

	# assuming ./image/ directory exists
	save_callback = get_save_state_callback('./image/', save_period, 
		settings.iterations, verbose=True)

	simulation_result = run_simulation(settings, callback=save_callback)
	simulation_result.save_JSON('result.json')
	simulation_result.plot_measures()
