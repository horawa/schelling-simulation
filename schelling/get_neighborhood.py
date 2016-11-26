def get_neighborhood(array, agent_index, radius=1):
	"""Get neighborhood of agent with specified radius.
	Neighboorhood a square with side 2*radius + 1 and center at agent_index.
	The retured neighborhood is a 2d list with preserved structure.
	The agent is not included in neighborhood.
	
	
	Args:
	    array (ndarray): array of agents
	    agent_index (tuple(int, int)): index of agent
	    radius (int, optional): radius of neighborhood
	
	Returns:
	    list: 2d list of neighbors with agent excluded
	"""
	array_rows = array.shape[0]
	array_cols = array.shape[1]

	row = agent_index[0]
	col = agent_index[1]

	if col - radius >= 0:
		lbound  = col - radius
		agent_to_remove_col = radius
	else:
		lbound = 0
		agent_to_remove_col = col
	
	if col + radius + 1 <= array_cols:
		rbound  = col + radius + 1 
	else:
		rbound = array_cols
	
	if row - radius >= 0:
		lobound = row - radius
		agent_to_remove_row = radius
	else:
		lobound = 0
		agent_to_remove_row = row
	
	if row + radius + 1 <= array_rows:
 		hibound = row + radius + 1
	else:
		hibound = array_rows


	neighborhood = array[lobound:hibound, lbound:rbound].tolist()
	neighborhood[agent_to_remove_row].pop(agent_to_remove_col)
	return neighborhood
