import numpy as np
from .array_utils import get_agent_indices

def get_neighborhood(array, agent_index, radius=1):
	"""Get neighborhood of agent with specified radius.
	Neighboorhood is a square with side 2*radius + 1 and center at agent_index.
	The retured neighborhood is a 2d array.	
	
	Args:
	    array (ndarray): array of agents
	    agent_index (tuple(int, int)): index of agent
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    ndarray: 2d array of neighbors with agent included
	"""
	array_rows = array.shape[0]
	array_cols = array.shape[1]

	row = agent_index[0]
	col = agent_index[1]

	if col - radius >= 0:
		lbound  = col - radius
	else:
		lbound = 0
	
	if col + radius + 1 <= array_cols:
		rbound  = col + radius + 1 
	else:
		rbound = array_cols
	
	if row - radius >= 0:
		lobound = row - radius
	else:
		lobound = 0

	if row + radius + 1 <= array_rows:
 		hibound = row + radius + 1
	else:
		hibound = array_rows

	neighborhood = array[lobound:hibound, lbound:rbound]
	return neighborhood


def get_neighborhood_exclusive(array, agent_index, radius=1):
	"""Get neighborhood of agent with specified radius.
	Neighboorhood is a square with side 2*radius + 1 and center at agent_index.
	The retured neighborhood is a 2d list with agent excluded -- structure is 
		not preserved.	
	
	Args:
	    array (ndarray): array of agents
	    agent_index (tuple(int, int)): index of agent
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    list: 2d list of neighbors with agent excluded
	"""

	row = agent_index[0]
	col = agent_index[1]

	if col - radius >= 0:
		agent_to_remove_col = radius
	else:
		agent_to_remove_col = col

	if row - radius >= 0:
		agent_to_remove_row = radius
	else:
		agent_to_remove_row = row


	neighborhood = get_neighborhood(array, agent_index, radius).tolist()
	neighborhood[agent_to_remove_row].pop(agent_to_remove_col)
	return neighborhood


def get_unlike_neighbor_fraction(array, agent_index, agent_type=None, radius=1, 
		count_vacancies=False):
	"""Get the fraction neighbors not of specified agent type in the 
	neighborhood  of the specified index. If agent type, is not given, 
	the agent type at specifed index will be used.
	
	Args:
	    array (ndarray): array
	    agent_index (tuple): index of agent in array
	    agent_type (int, optional): Type of agent
	    radius (int, optional): Radius of neighborhood
	
	Returns:
	    float: The fraction of neighbors not of specified type
	"""
	if agent_type is None:
		agent_type = array[tuple(agent_index)]

	neighborhood = get_neighborhood(array, tuple(agent_index), radius)

	not_vacant = neighborhood != 0

	if count_vacancies:
		neighbor_count = neighborhood.size - 1
	else:
		neighbor_count = np.count_nonzero(not_vacant)
		if array[tuple(agent_index)] != 0:
			neighbor_count -= 1 # agent will be excluded from neighbor count

	unlike_agent_count = np.count_nonzero(np.logical_and(not_vacant, 
		neighborhood != agent_type))

	# if agent has no neighbors - unlike neighbor fraction = 0
	if neighbor_count == 0:
		return 0.0

	unlike_agent_fraction = unlike_agent_count / neighbor_count

	return unlike_agent_fraction


