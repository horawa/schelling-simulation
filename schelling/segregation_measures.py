from math import log, isclose
import numpy as np
from scipy.ndimage.measurements import label

from .neighborhood import (get_neighborhood, get_neighborhood_exclusive, 
	get_unlike_neighbor_fraction)


def _get_measure_average(array, agent_indices, measure_func):
	"""Get average of fuction results for each index in array
	
	Args:
	    array (ndarray): array
	    measure_func (function): (2d array, indexes tuple) -> value
	
	Returns:
	    number: average function value
	"""
	total = sum(measure_func(array, tuple(index)) for index in agent_indices)

	return total / agent_indices.shape[0]


def entropy_average(array, agent_indices, radius=1):
	"""Returns average of entropies for all agents in array.
	See entropy
	
	Args:
	    array (ndarray): array of agents
	   	agent_indices (ndarray): indices of agents in the format 
	   		[[row, col], [row, col], ...]
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    float: average entropy
	"""
	entropy_average = _get_measure_average(array, agent_indices, 
		lambda a, i: entropy(a, i, radius))
	return entropy_average


def switch_rate_average(array, agent_indices):
	"""Returns average of switch rates for all agents in array.
	See switch_rate

	Args:
	    array (ndarray): array of agents
	   	agent_indices (ndarray): indices of agents in the format 
	   		[[row, col], [row, col], ...]
	
	Returns:
	    float: average switch rate
	"""
	return _get_measure_average(array, agent_indices, switch_rate)


def distance_average(array, agent_indices):
	return _get_measure_average(array, agent_indices, distance)


def mix_deviation_average(array, agent_indices, radius=1):
	def mix_deviation_for_radius(array, agent_index):
		return mix_deviation(array, agent_index, radius)

	return _get_measure_average(array, agent_indices, mix_deviation_for_radius)


def switch_rate(array, agent_index):
	"""Calculates switch rate for agent at specified index in array
	Switch rate: Turn around an agent full circle. 
		How many times does the type of neighbor switch?
	Args:
	    array (ndarray): array of agents
	    agent_index (tuple(int, int)): index of agent
	
	Returns:
	    int: Switch rate
	"""
	# TODO reimplement to get rid of get_neighborhood_exclusive
	# TODO count vacancies ?
	array_rows = array.shape[0]
	array_cols = array.shape[1]

	row = agent_index[0]
	col = agent_index[1]

	neighborhood = get_neighborhood_exclusive(array, agent_index)

	if len(neighborhood) == 3:
		top = neighborhood[0]
		bottom = neighborhood[2][::-1]
		if len(neighborhood[1]) == 2:
			left = [neighborhood[1][0]]
			right = [neighborhood[1][1]]
		elif col == 0:
			left = []
			right = neighborhood[1]
		else:
			left = neighborhood[1]
			right = []
		neighbors = top + right + bottom + left
	else:
		neighbors = neighborhood[0] + neighborhood[1][::-1]

	switch_count = 0
	for agent, next_agent in zip(neighbors, neighbors[1:] + [neighbors[0]]):
		if agent != next_agent:
			switch_count += 1

	return switch_count


def entropy(array, agent_index, radius=1, count_vacancies=False):
	"""Calculates the entropy in the neighborhood of specified agent
	Entropy = sum of pi * log2pi
	Where i - agent type, pi = (agents of type i)/(all agents in neighborhood)

	Args:
	    array (ndarray): array of agents
	    agent_index (tuple(int, int)): index of agent
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    float: Entropy of agent's neighborhood
	"""
	# TODO should I include agent?; should I include vacancies?
	agent_type = array[agent_index]
	neighborhood = get_neighborhood(array, agent_index, radius)


	if count_vacancies:
		total_neighbors = neighborhood.size - 1 # excluding agent
	else:
		total_neighbors = np.count_nonzero(neighborhood != 0)
		if agent_type != 0:
			total_neighbors -= 1

	neighbor_types = np.unique(neighborhood)
	if not count_vacancies and 0 in neighbor_types:
		neighbor_types = neighbor_types[1:] # exclude vacancies

	entropy = 0
	for neighbor_type in neighbor_types:
		neighbor_type_count = np.count_nonzero(neighborhood == neighbor_type)
		# exclude agent
		if neighbor_type == agent_type:
			neighbor_type_count -= 1
			# if agent is the only one of its type, do not include
			if neighbor_type_count == 0:
				continue

		p_neighbor_type = neighbor_type_count / total_neighbors

		# entropy = -sum_i(p_i * log2 p_i)
		entropy -= (p_neighbor_type * log(p_neighbor_type, 2))

	return entropy


def ghetto_rate(array, agent_indices, radius=1):
	agents_in_ghettos = 0
	for agent_index in agent_indices:
		is_in_ghetto = isclose(
			get_unlike_neighbor_fraction(array, agent_index), 0.0)
		if is_in_ghetto:
			agents_in_ghettos += 1

	ghetto_rate = agents_in_ghettos / agent_indices.shape[0]

	return ghetto_rate


def clusters(array):
	#TODO cache agent types
	agent_types = np.unique(array)[1:]
	total_clusters = 0
	for agent_type in agent_types:
		labelled, cluster_count = label(np.where(array == agent_type, 1, 0))
		total_clusters += cluster_count

	return total_clusters


def distance(array, agent_index):
	agent_type = array[tuple(agent_index)]

	distance = 1
	while distance <= array.shape[0]:
		neighborhood = get_neighborhood(array, agent_index, radius=distance)
		if np.any(
				np.logical_and(neighborhood != agent_type, neighborhood != 0)):
			break
		distance += 1

	return distance


def mix_deviation(array, agent_index, radius=1):
	# TODO cache unlike neighbor fraction
	mix_neigbbor_fraction = 0.5
	unlike_neighbor_fraction = get_unlike_neighbor_fraction(
		array, tuple(agent_index), radius=radius)

	mix_deviation = abs(mix_neigbbor_fraction - unlike_neighbor_fraction)

	return mix_deviation
