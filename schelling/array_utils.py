import numpy as np

def get_agent_indices(array):
	"""Get indices of agents in array
	
	Args:
	    array (ndarray): array
	
	Returns:
	    ndarray: array of indices
	"""	
	agent_indices = np.argwhere(array != 0)
	return agent_indices


def get_agent_indices_of_type(array, agent_type):
	"""Get indices of agents in array
	
	Args:
	    array (ndarray): array
	    agent_type (int): type of agent
	
	Returns:
	    ndarray: array of indices
	"""	
	agent_indices = np.argwhere(array == agent_type)
	return agent_indices


def get_vacancy_indices(array):
	"""Get indices of vacancies in array
	
	Args:
	    array (ndarray): array
	
	Returns:
	    ndarray: array of indices
	"""	
	vacancy_indices = np.argwhere(array == 0)
	return vacancy_indices