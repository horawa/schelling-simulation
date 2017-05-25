import numpy as np
import numpy.random as rand
import math
import os
import click

from schelling.array_utils import get_agent_indices, get_vacancy_indices
from schelling.utility_functions import get_utility_for_array
from schelling.create_array import create_array
from schelling.simulation_result import SimulationResult
from schelling.arr_to_img import to_image, image_save
import schelling.segregation_measures as sm

_stop = False
_pause = False


def stop():
	global _stop
	_stop = True

def pause():
	global _pause
	_pause = True

def unpause():
	global _pause
	_pause = False


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
	global _stop


	settings.validate()
	result = SimulationResult(settings.segregation_measure_names)

	array = create_array(settings.grid_size, 
		settings.get_agent_type_proportions(), 
		settings.initial_random_allocation)

	# utility - function: (index) -> (0,1)
	utility = get_utility_for_array(settings.utility_function, array, 
		count_vacancies=settings.count_vacancies, radius=settings.radius)

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

	# if no agents, end simulation
	agent_indices = get_agent_indices(array)
	if agent_indices.shape[0] == 0:
		return result

	# _update_result(result, array, agent_indices,
		# settings.count_vacancies, settings.segregation_measure_names)

	for i in range(settings.iterations):

		while _pause:
			pass


		should_save_result = i % settings.save_period == 0

		if should_save_result:
			callback(array, result, i)

		is_simulation_halted = update_array(array, utility, 
			result, agent_picker, vacancy_picker, settings.count_vacancies, 
			settings.segregation_measure_names, settings.satisficers,
			should_save_result)

		# if no further moves are possible, exit simulation early
		if is_simulation_halted:
			# Get measures for final state and save (unless it was just saved)
			if not should_save_result:
				agent_indices = get_agent_indices(array)
				_update_result(result, array, agent_indices, 
					settings.count_vacancies, settings.segregation_measure_names)
				callback(array, result, i)
			break

		if _stop:
			break

	_stop = False

	return result


def update_array(array, utility, result, agent_picker, 
	vacancy_picker, count_vacancies, segregation_measure_names,
	satisficers=False, save_result=True):
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

	if save_result:
		_update_result(result, array, agent_indices, count_vacancies, 
			segregation_measure_names)
	
	unsatisfied_agent_indices = _get_unsatisfied_agent_indices(utility, 
		agent_indices, satisficers=satisficers)

	# if all agents satisfied, end simulation
	if unsatisfied_agent_indices.size == 0:
		return True

	agent_index = _pick_agent_index_to_move(unsatisfied_agent_indices, 
		agent_picker)

	vacancy_indices = get_vacancy_indices(array)
	if vacancy_indices.size == 0:
		return True

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


def _update_result(result, array, agent_indices, count_vacancies, 
		segregation_measure_names):
	"""Store current segregation measures in segregation result object
	
	Args:
	    result (SegregationResult): result object
	    array (ndarray): array
	    agent_indices (ndarray): indices of agents in array
	"""
	for segregation_measure_name in segregation_measure_names:
		if segregation_measure_name == 'entropy_average':
			value = sm.segregation_measures['entropy_average'](
				array, agent_indices, count_vacancies=count_vacancies)
		elif segregation_measure_name == 'clusters':
			value = sm.segregation_measures['clusters'](array)
		else:
			value = sm.segregation_measures[segregation_measure_name](
				array, agent_indices)

		result.save_measure(segregation_measure_name, value)


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


def get_save_state_callback(save_directory, iterations, verbose=False):
	iter_order_of_magnitude = int(math.log10(iterations)) + 1
	def save_state(array, result, iteration):
		file_name = str(iteration).zfill(iter_order_of_magnitude + 1) + '.png'
		image_save(to_image(array), 
			os.path.join(save_directory, file_name))
		result.save_JSON(os.path.join(save_directory, 'result.json'))
		if verbose:
			click.echo(iteration)
			click.echo(result)
	return save_state


def is_simulation_halted(array, utility_function):

	utility = get_utility_for_array(utility_function, array, count_vacancies=True)
	agent_indices = get_agent_indices(array)

	if agent_indices.size == 0:
		return True

	unsatisfied_agent_indices = _get_unsatisfied_agent_indices(utility, agent_indices, satisficers=False)
	if unsatisfied_agent_indices.size == 0:
			return True		

	vacancy_indices = get_vacancy_indices(array)
	
	if vacancy_indices.size == 0:
		return True

	for agent_index in unsatisfied_agent_indices:
		better_vacancies = _get_better_vacancies(array, agent_index, utility, vacancy_indices, satisficers=False)
		if better_vacancies.size != 0:
			return False
	return True


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
			iterations=10000,
			save_period=100
		)

	# assuming ./image/ directory exists
	save_callback = get_save_state_callback('./image/', settings.iterations, 
		verbose=True)

	simulation_result = run_simulation(settings, callback=save_callback)
	simulation_result.save_JSON('result.json')
	simulation_result.plot_measures()
