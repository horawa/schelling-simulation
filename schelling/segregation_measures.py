from math import log
from itertools import chain
from numpy import unique
from .get_neighborhood import get_neighborhood


def _get_measure_average(array, measure_func):
	"""Get average of fuction results for each index in array
	
	Args:
	    array (ndarray): array
	    measure_func (function): (2d array, indexes tuple) -> value
	
	Returns:
	    number: average function value
	"""
	array_rows = array.shape[0]
	array_cols = array.shape[1]

	indexes = zip(range(array_rows), range(array_cols))
	total = sum(measure_func(array, index) for index in indexes)

	return total / array.size


def entropy_average(array, radius=1):
	"""Returns average of entropies for all agents in array.
	See entropy
	
	Args:
	    array (ndarray): array of agents
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    float: average entropy
	"""
	return _get_measure_average(array, lambda a, i: entropy(a, i, radius))


def switch_rate_average(array, radius=1):
	"""Returns average of switch rates for all agents in array.
	
	Args:
	    array (ndarray): array of agents
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    float: average switch rate
	"""
	return _get_measure_average(array, switch_rate)



def switch_rate(array, agent_index):
	"""Calculates switch rate for agent at specified index in array
	Switch rate: Turn around an agent. How many times does the type of neighbor switch
	Args:
	    array (ndarray): array of agents
	    agent_index (tuple(int, int)): index of agent
	
	Returns:
	    int: Switch rate
	"""
	array_rows = array.shape[0]
	array_cols = array.shape[1]

	row = agent_index[0]
	col = agent_index[1]

	neighborhood = get_neighborhood(array, agent_index)

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


def entropy(array, agent_index, radius=1):
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
	neighborhood = get_neighborhood(array, agent_index, radius)

	neighbors = list(chain.from_iterable(neighborhood))
	total_neighbors = len(neighbors)

	agent_types = set(neighbors)
	if 0 in agent_types:
		agent_types.remove(0)


	# entropy = -sum_i(p_i * ln pi)
	p_agent_type = (neighbors.count(agent_type) / total_neighbors for agent_type in agent_types)
	entropy = -sum(p_a * log(p_a, 2) for p_a in p_agent_type)

	return entropy
