import numpy as np

# TODO test with size 38

def create_array(size, agent_type_fractions, random_allocation=True):
	"""Creates a square 2d numpy array representing a 2d grid randomly populated by agents.
	Nodes with value 0 are vacant
	Nodes with value n are occupied by agent of type n (n - integer value)
	If random_allocation is false, agents will be segregated in clusters

	Example:
	create_array(50, (0.2, 0.5, 0.3)) will create a grid of 50*50 = 2500 spots.
	0.2 * 2500 = 500 will be vacant
	0.5 * 2500 = 1250 will be occupied by agents of type 1.
	0.4 * 2500 = 750 will be occupied by agents of type 2.
	
	Args:
	    size (int): size of grid side
	    agent_type_fractions (tuple of float): fraction of each agent type. 
	    	First element represents fraction of vacancies.
	    	Subsequent elements represent fractions of agents of each type
	    random_allocation (bool): Agents will be allocated at random if true, 
	    	or segregated, if false
	
	Returns:
	    ndarray: array representing 2d grid randomly populated by agents
	"""
	if float(sum(agent_type_fractions)) != 1.0:
		raise ValueError("agent type fractions must sum up to 1")

	n_cells = size * size
	
	agent_type_counts = [int(n_cells * agent_type_fraction) 
	  for agent_type_fraction in agent_type_fractions]

	array_data = []
	for agent_type_index, agent_type_count in enumerate(agent_type_counts):
		array_data += ([agent_type_index] * agent_type_count)

	# The number of cells could be less than 
	# size*size due to rounding down floats.
	# In that case, prepend additional vacant slots.
	while len(array_data) != n_cells:
		array_data = [0] + array_data

	array = np.array(array_data)

	if random_allocation:
		np.random.shuffle(array)
	
	array = array.reshape((size, size))
	return array
